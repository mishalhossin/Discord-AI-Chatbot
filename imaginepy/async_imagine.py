import io

import aiohttp
from langdetect import detect
import traceback
import asyncio

from .constants import *

def validate_cfg(cfg: str) -> float:
    """Validates the cfg parameter."""
    cfg_float = float(cfg)
    if cfg_float < 0.0 or cfg_float > 16.0:
        raise ValueError(f"Invalid CFG, must be in range (0; 16), {cfg_float}")
    return cfg_float
# def validate_cfg(cfg: float) -> str:
#     """Validates the cfg parameter."""
#     if cfg < 0.0 or cfg > 16.0:
#         raise ValueError(f"Invalid CFG, must be in range (0; 16), {cfg}")
#     return str(cfg)


class AsyncImagine:
    """Async class for handling API requests to the Imagine service."""

    HEADERS = {
        "accept": "*/*",
        "user-agent": "okhttp/4.10.0",
        "style-id":"30"
    }

    def __init__(self,style = None):
        self.asset = "https://1966211409.rsc.cdn77.org"
        self.api = "https://inferenceengine.vyro.ai"
        if style is not None:
            self.HEADERS["style-id"] = str(style.value[0])
        self.session = aiohttp.ClientSession(raise_for_status=True, headers=self.HEADERS)
        self.version = "1"

    async def close(self) -> None:
        """Close async session"""
        return await self.session.close()

    def get_style_url(self, style: Style = Style.IMAGINE_V1) -> str:
        """Get link of style thumbnail"""
        return f"{self.asset}/appStuff/imagine-fncisndcubnsduigfuds//assets/{style.value[2]}/{style.value[1]}.webp"

    def bytes_to_io(self, data: bytes, filename: str) -> io.BytesIO:
        """Convert bytes to io.BytesIO with name for sending"""
        bio = io.BytesIO(data)
        bio.name = filename
        return bio

    async def assets(self, style: Style = Style.IMAGINE_V1) -> bytes:
        """Gets the assets."""
        async with self.session.get(
                url=self.get_style_url(style=style)
        ) as resp:
            return await resp.read()

    async def sdprem(self, prompt: str, negative: str = None, priority: str = None, steps: str = None,
                    high_res_results: str = None, style: Style = Style.IMAGINE_V1, seed: str = None,
                    ratio: Ratio = Ratio.RATIO_1X1, cfg: str = "9.5") -> bytes:
        """Generates AI Art."""
        if style is not None:
            self.HEADERS["style-id"] = str(style.value[0])
        cfg = float(cfg)
        try:
            validated_cfg = validate_cfg(cfg)
        except Exception as e:
            print(f"An error occurred while validating cfg: {e}")
            traceback.print_exc()  # Print the full traceback for detailed debugging
            return None

        for attempt in range(2):
            try:
                async with self.session.post(
                        url=f"{self.api}/sdprem",
                        data={
                            "model_version": self.version,
                            "prompt": prompt + (style.value[3] or ""),
                            "negative_prompt": negative or "ugly, disfigured, low quality, blurry, nsfw",
                            "style_id": style.value[0],
                            "aspect_ratio": f"{ratio.value[0]}:{ratio.value[1]}",
                            "seed": seed or "",
                            "steps": steps or "30",
                            "cfg": validated_cfg,
                            "priority": priority or "0",
                            "high_res_results": high_res_results or "0"
                        }
                ) as resp:
                    return await resp.read()
            except Exception as e:
                print(f"An error occurred while making the request: {e}")
                traceback.print_exc()  # Print the full traceback for detailed debugging
                if attempt == 0:
                    await asyncio.sleep(0.4)
                    print("Retrying....")
                else:
                    return None

    async def upscale(self, image: bytes) -> bytes:
        """Upscales the image."""
        try:
            async with self.session.post(
                    url=f"{self.api}/upscale",
                    data={
                        "model_version": self.version,
                        "image": self.bytes_to_io(image, "test.png")
                    }
            ) as resp:
                return await resp.read()
        except Exception as e:
            print(f"An error occurred while making the request: {e}")
            return None
            
    async def interrogator(self, image: bytes) -> str:
        """Generates a prompt."""
        async with self.session.post(
                url=f"{self.api}/interrogator",
                data={
                    "model_version": str(self.version),
                    "image": self.bytes_to_io(image, "prompt_generator_temp.png")
                }
        ) as resp:
            return await resp.text()

    async def sdimg(self, image: bytes, prompt: str, negative: str = None, seed: str = None, cfg: float = 9.5) -> bytes:
        """Performs inpainting."""
        async with self.session.post(
                url=f"{self.api}/sdimg",
                data={
                    "model_version": self.version,
                    "prompt": prompt,
                    "negative_prompt": negative or "",
                    "seed": seed or "",
                    "cfg": validate_cfg(cfg),
                    "image": self.bytes_to_io(image, "image.png")
                }
        ) as resp:
            return await resp.read()
