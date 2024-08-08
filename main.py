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

# Adding Frame
pil_image = Image.open(filename)

width, height = [int(dim * config["resize_factor"]) for dim in pil_image.size]
framed_width = width + 2 * config["side_padding"]
framed_height = height + config["top_padding"] + config["bottom_padding"]

framed_image = Image.new(
    pil_image.mode, (framed_width, framed_height), tuple(config["frame_color"])
)
framed_image.paste(
    pil_image.resize((width, height), Image.LANCZOS),
    (config["side_padding"], config["top_padding"]),
)

framed_image.show()
