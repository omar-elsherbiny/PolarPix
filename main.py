import json
import exiv2

config = {}
with open("config.json", "r") as config_file:
    config = json.load(config_file)

filename = "img.jpg"
image = exiv2.ImageFactory.open(filename)
exiv2.enableBMFF()
image.readMetadata()
data = image.exifData()
for key in data:
    print(key)
