from typing import Any, Optional, Tuple
from requests import Session, Response
from requests_toolbelt.multipart.encoder import MultipartEncoder
from langdetect import detect

from .constants import *


def validate_cfg(cfg: float) -> str:
    """Validates the cfg parameter."""
    if cfg < 0.0 or cfg > 16.0:
        raise ValueError(f"Invalid CFG, must be in range (0; 16), {cfg}")
    return str(cfg)


class Imagine:
    """Class for handling API requests to the Imagine service."""

    HEADERS = {
        "accept": "*/*",
        "user-agent": "okhttp/4.10.0"
    }

    def __init__(self):
        self.asset = "https://1966211409.rsc.cdn77.org"
        self.api = "https://inferenceengine.vyro.ai"
        self.session = Session()
        self.version = "1"

    def _request(self, **kwargs) -> Response:
        """Sends a request to the server and returns the response."""
        headers = Imagine.HEADERS.copy()
        headers.update(kwargs.get("headers", {}))

        response = self.session.request(
            method=kwargs.get("method", "GET").upper(),
            url=kwargs.get("url"),
            params=kwargs.get("params"),
            data=kwargs.get("data"),
            headers=headers
        )

        response.raise_for_status()
        return response

    def _build_multipart_data(self, fields: dict) -> Tuple[MultipartEncoder, dict]:
        """Helper function to build multipart form data."""
        multi = MultipartEncoder(fields=fields)
        headers = {"content-type": multi.content_type}
        return multi, headers

    def assets(self, style: Style = Style.IMAGINE_V1) -> bytes:
        """Gets the assets."""
        return self._request(
            url=f"{self.asset}/appStuff/imagine-fncisndcubnsduigfuds//assets/{style.value[2]}/{style.value[1]}.webp"
        ).content

    def variate(self, image: bytes, prompt: str, style: Style = Style.IMAGINE_V1) -> bytes:
        """Variates the character."""
        multi, headers = self._build_multipart_data({
            "model_version": self.version,
            "prompt": prompt + (style.value[3] or ""),
            "strength": "0",
            "style_id": str(style.value[0]),
            "image": ("image.png", image, "image/png")
        })

        return self._request(
            method="POST",
            url=f"{self.api}/variate",
            data=multi,
            headers=headers
        ).content

    def sdprem(self, prompt: str, negative: str = None, priority: str = None, steps: str = None, high_res_results: str = None, style: Style = Style.IMAGINE_V1, seed: str = None, ratio: Ratio = Ratio.RATIO_1X1, cfg: float = 9.5) -> bytes:
        """Generates AI Art."""
        try:
            validated_cfg = validate_cfg(cfg)
        except Exception as e:
            print(f"An error occurred while validating cfg: {e}")
            return None

        try:
            return self._request(
                method="POST",
                url=f"{self.api}/sdprem",
                data={
                    "model_version": self.version,
                    "prompt": prompt + (style.value[3] or ""),
                    "negative_prompt": negative or "",
                    "style_id": style.value[0],
                    "width": ratio.value[0],
                    "height": ratio.value[1],
                    "seed": seed or "",
                    "steps": steps or "30",
                    "cfg": validated_cfg,
                    "priority": priority or "0",
                    "high_res_results": high_res_results or "0"
                }
            ).content
        except Exception as e:
            print(f"An error occurred while making the request: {e}")
            return None

    def upscale(self, image: bytes) -> bytes:
        """Upscales the image."""
        try:
            multi, headers = self._build_multipart_data({
                "model_version": self.version,
                "image": ("test.png", image, "image/png")
            })
        except Exception as e:
            print(f"An error occurred while building the multipart data: {e}")
            return None

        try:
            return self._request(
                method="POST",
                url=f"{self.api}/upscale",
                data=multi,
                headers=headers
            ).content
        except Exception as e:
            print(f"An error occurred while making the request: {e}")
            return None

    def translate(self, prompt: str) -> str:
        """Translates the prompt."""
        multi, headers = self._build_multipart_data({
            "q": prompt,
            "source": detect(prompt),
            "target": "en"
        })

        return self._request(
            method="POST",
            url=f"{self.api}/translate",
            data=multi,
            headers=headers
        ).json()["translatedText"]

    def interrogator(self, image: bytes) -> str:
        """Generates a prompt."""
        multi, headers = self._build_multipart_data({
            "model_version": str(self.version),
            "image": ("prompt_generator_temp.png", image, "application/zip")
        })

        return self._request(
            method="POST",
            url=f"{self.api}/interrogator",
            data=multi,
            headers=headers
        ).text

    def sdimg(self, image: bytes, prompt: str, negative: str = None, seed: str = None, cfg: float = 9.5) -> bytes:
        """Performs inpainting."""
        multi, headers = self._build_multipart_data({
            "model_version": self.version,
            "prompt": prompt,
            "negative_prompt": negative or "",
            "seed": seed or "",
            "cfg": validate_cfg(cfg),
            "image": ("image.png", image, "image/png")
        })

        return self._request(
            method="POST",
            url=f"{self.api}/sdimg",
            data=multi,
            headers=headers
        ).content

    def controlnet(self, image: bytes, prompt: str, negative: str = None, cfg: float = 9.5, control: Control = Control.SCRIBBLE, style: Style = Style.IMAGINE_V1, seed: str = None) -> bytes:
        """Performs image remix."""
        multi, headers = self._build_multipart_data({
            "model_version": self.version,
            "prompt": prompt + (style.value[3] or ""),
            "negative_prompt": negative or "",
            "strength": "0",
            "cfg": validate_cfg(cfg),
            "control": control.value,
            "style_id": str(style.value[0]),
            "seed": seed or "",
            "image": ("image.png", image, "image/png")
        })

        return self._request(
            method="POST",
            url=f"{self.api}/controlnet",
            data=multi,
            headers=headers
        ).content

