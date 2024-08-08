import json
import exiv2
from PIL import Image, ImageDraw, ImageFont

filename = "img.jpg"
output_file = "res.jpg"

# Loading Config
config = {}
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Extracting MetaData
exiv2.enableBMFF()
exiv_image = exiv2.ImageFactory.open(filename)
exiv_image.readMetadata()
metadata = exiv_image.exifData()
metadata_keys = [str(key).split(":") for key in metadata]
metadata = {
    x[0].replace("Exif.", "").strip(): ":".join(x[1:]).strip() for x in metadata_keys
}
[print(f"{key: <40}  {metadata[key]: >20}") for key in metadata]

# Adding Frame
pil_image = Image.open(filename)

width, height = [int(dim * config["resize_factor"]) for dim in pil_image.size]
framed_width = width + 2 * config["side_padding"]
framed_height = (
    height
    + config["top_margin"]
    + config["top_padding"]
    + config["bottom_padding"]
    + config["bottom_margin"]
)

framed_image = Image.new(
    pil_image.mode, (framed_width, framed_height), tuple(config["frame_color"])
)
framed_image.paste(
    pil_image.resize((width, height), Image.LANCZOS),
    (config["side_padding"], config["top_margin"] + config["top_padding"]),
)

# Adding Text
drawn_image = ImageDraw.Draw(framed_image)
font1 = ImageFont.truetype("MonaSans-Medium.ttf", 65)
font2 = ImageFont.truetype("MonaSans-Regular.ttf", 40)

drawn_image.text(
    (config["side_padding"] + config["text_side_offset"], config["top_margin"]),
    metadata["Photo.LensModel"],
    font=font1,
    fill=tuple(config["text_color"]),
)

drawn_image.text(
    (
        config["side_padding"] + config["text_side_offset"],
        config["top_margin"]
        + font1.getbbox(metadata["Photo.LensModel"])[3]
        + config["text_vertical_spacing"],
    ),
    metadata["Image.Model"],
    font=font2,
    fill=tuple(config["text_color"]),
)

right_offset = (
    framed_width
    - config["side_padding"]
    - config["text_side_offset"]
    - font1.getbbox("ISO" + metadata["Photo.ISOSpeedRatings"])[2]
)

drawn_image.text(
    (
        right_offset,
        config["top_margin"],
    ),
    "ISO" + metadata["Photo.ISOSpeedRatings"],
    font=font1,
    fill=tuple(config["text_color"]),
)

right_offset -= (
    config["text_horizontal_spacing"]
    + font1.getbbox(metadata["Photo.ShutterSpeedValue"].replace(" ", ""))[2]
)

drawn_image.text(
    (
        right_offset,
        config["top_margin"],
    ),
    metadata["Photo.ShutterSpeedValue"].replace(" ", ""),
    font=font1,
    fill=tuple(config["text_color"]),
)

right_offset -= (
    config["text_horizontal_spacing"]
    + font1.getbbox(metadata["Photo.ApertureValue"])[2]
)

drawn_image.text(
    (
        right_offset,
        config["top_margin"],
    ),
    metadata["Photo.ApertureValue"],
    font=font1,
    fill=tuple(config["text_color"]),
)

right_offset -= (
    config["text_horizontal_spacing"]
    + font1.getbbox(metadata["Photo.FocalLength"].replace(" ", ""))[2]
)

drawn_image.text(
    (
        right_offset,
        config["top_margin"],
    ),
    metadata["Photo.FocalLength"].replace(" ", ""),
    font=font1,
    fill=tuple(config["text_color"]),
)

drawn_image.text(
    (
        framed_width
        - config["side_padding"]
        - config["text_side_offset"]
        - font2.getbbox(metadata["Photo.DateTimeOriginal"])[2],
        config["top_margin"]
        + font1.getbbox(metadata["Photo.LensModel"])[3]
        + config["text_vertical_spacing"],
    ),
    metadata["Photo.DateTimeOriginal"],
    font=font2,
    fill=tuple(config["text_color"]),
)

framed_image.show()
