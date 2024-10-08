# PolarPix
Saw a some photographers on reddit posting photos in a similar format, so I decided to automate it in python!

credits to: [JohnnyFootball16](https://www.reddit.com/r/SonyAlpha/comments/1em4g9k/first_try_at_night_photography/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button) for the inspiration
# Dependancies
Install all required dependencies with pip using:
```bash
pip install exiv2 Pillow colorthief
```
# Usage
Run either the python file or the exe in the same directory as the font files and `config.json`<br>

A file selection dialog will appear, select your input file that has metadata<br>

A second dialog will appear, select your output file in you desired image format

After the script runs a popup of the new image will appear and the output file will be saved

# Configuration
Use the `config.json` file to format the picture as you want

- `top_margin` and `bottom_margin` are the amount of pixels framing the picture at the top and bottom

- `top_padding` and `bottom_padding` are the amount of pixels at the top and bottom of the picture that will be added to fit the text and the pallete
- `side_padding` is the amount of pixels at either side of the frame
- `text_vertical_spacing` is the spacing in pixels between the first and second line of metadata
- `text_horizontal_spacing` is the spacing in pixels between the individual pieces of data
- `text_side_offset` is the amount of pixels the text will be offset from the side padding, bringing the text closer to the center
- `palette_height` is the height in pixels that will be taken up from the bottom padding to view the pallete
- `frame_color` and `text_color` are RGB values of the the frame and text
- `resize_factor` is the ratio the original photo will be scaled in the formated picture
- `font_file_1` and `font_file_2` are the paths to the '.ttf' files that are used to display the first and second lines of metadata
- `font_size_1` and `font_size_2` are the font sizes of the first and second lines of metadata
- `pallete_color_count` is the number of color that are gonna be picked in the pallete

# Examples
![res](https://github.com/user-attachments/assets/ebd9f0b0-4a89-4276-90f9-e95fc2123354)
![res1](https://github.com/user-attachments/assets/d5ef80b6-c9d8-49f9-a5df-72603af8e314)
![res2](https://github.com/user-attachments/assets/ad781d18-f8c8-4d02-ad7c-8061025893d2)
![res3](https://github.com/user-attachments/assets/78ff506a-9e0d-4445-af83-82ea9abb1155)
