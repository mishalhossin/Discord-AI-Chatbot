from imaginepy import Imagine, Style, Ratio

def main():
    imagine = Imagine()

    img_data = imagine.sdprem(
        prompt="Woman sitting on a table, looking at the sky, seen from behind",
        style=Style.ANIME_V2,
        ratio=Ratio.RATIO_16X9
    )

    if img_data is None:
        print("An error occurred while generating the image.")
        return

    try:
        with open("example.png", mode="wb") as img_file:
            img_file.write(img_data)
    except Exception as e:
        print(f"An error occurred while writing the image to file: {e}")

if __name__ == "__main__":
    main()
