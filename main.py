import json
import exiv2
from PIL import Image, ImageDraw, ImageFont
from colorthief import ColorThief
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()
filename = askopenfilename(
    defaultextension="*.jpg",
    filetypes=[
        (
            "Input Image",
            ("*.tif", "*.tiff", "*.png", "*.jpg", "*.jpeg", "*.JPG", "*.JPEG"),
        )
    ],
)

if not filename:
    raise Exception("Filename can't be empty")

output_file = askopenfilename(
    defaultextension="*.jpg",
    filetypes=[("Output Image", "*")],
)

if not output_file:
    raise Exception("Filename can't be empty")


# Loading Config
config = {}
with open("config.json", "r") as config_file:
    config = json.load(config_file)
    for key, value in config.items():
        if type(value) == int:
            config[key] = max(0, value)

# Extracting MetaData
exiv2.enableBMFF()
exiv_image = exiv2.ImageFactory.open(filename)
exiv_image.readMetadata()
metadata = exiv_image.exifData()
metadata_keys = [str(key).split(":") for key in metadata]
metadata = {
    x[0].replace("Exif.", "").strip(): ":".join(x[1:]).strip() for x in metadata_keys
}

if not metadata:
    raise Exception("No available metadata")

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
font1 = ImageFont.truetype(config["font_file_1"], config["font_size_1"])
font2 = ImageFont.truetype(config["font_file_2"], config["font_size_2"])

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

# Adding Palette
palette = ColorThief(filename).get_palette(
    color_count=config["palette_color_count"], quality=10
)

swatch_width = width / config["palette_color_count"]
left_offset = config["side_padding"]
top_offset = (
    config["top_margin"] + config["top_padding"] + height + config["bottom_padding"]
)

for i in range(min(len(palette), config["palette_color_count"])):
    drawn_image.rectangle(
        [
            (left_offset, top_offset - config["palette_height"]),
            (left_offset + swatch_width, top_offset),
        ],
        fill=palette[i],
    )
    left_offset += swatch_width

framed_image.show()
framed_image.save(output_file, exif=pil_image.getexif())
