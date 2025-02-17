# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os
from typing import TYPE_CHECKING, Any

import numpy as np
from PIL import Image, ImageDraw

import streamlit as st

if TYPE_CHECKING:
    import numpy.typing as npt


# Construct test assets path relative to this script file to
# allow its execution with different working directories.
TEST_ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "test_assets"
)

img = np.repeat(0, 10000).reshape(100, 100)
img800 = np.repeat(0, 640000).reshape(800, 800)


st.header("Images from numpy arrays")

st.image(img, caption="Black Square as JPEG.", output_format="JPEG", width=100)

st.image(img, caption="Black Square as PNG.", output_format="PNG", width=100)

st.image(img, caption="Black Square with no output format specified.", width=100)

transparent_img: "npt.NDArray[Any]" = np.zeros((100, 100, 4), dtype=np.uint8)
st.image(transparent_img, caption="Transparent Black Square.", width=100)

st.header("GIF images")


def create_gif(size, frames=1):
    # Create grayscale image.
    im = Image.new("L", (size, size), "white")

    images = []

    # Make circle of a constant size with a number of frames, moving across the
    # principal diagonal of a 64x64 image. The GIF will not loop and stops
    # animating after frames x 100ms.
    for i in range(frames):
        frame = im.copy()
        draw = ImageDraw.Draw(frame)
        pos = (i, i)
        circle_size = size / 2
        draw.ellipse([pos, tuple(p + circle_size for p in pos)], "black")
        images.append(frame.copy())

    # Save the frames as an animated GIF
    data = io.BytesIO()
    images[0].save(
        data,
        format="GIF",
        save_all=True,
        append_images=images[1:],
        duration=1,
    )

    return data.getvalue()


gif = create_gif(64, frames=32)

st.image(gif, caption="Moving black circle.", width=100)
st.image(create_gif(64), caption="Black Circle as GIF.", width=100)
st.image(gif, caption="GIF as PNG.", output_format="PNG", width=100)

st.header("SVG images")

st.image(
    """<?xml version="1.0" encoding="utf-8"?>
    <!-- Generator: Adobe Illustrator 17.1.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="500" height="100">
    <text x="0" y="50">"I am prefixed with some meta tags</text>
    </svg>
""",
    caption="Text SVG with meta tags.",
)


st.image(
    """
<svg>
  <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
  Sorry, your browser does not support inline SVG.
</svg>
""",
    caption="Red Circle.",
)

SVG_RED_CIRCLE = """
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
  Sorry, your browser does not support inline SVG.
</svg>
"""

st.image(SVG_RED_CIRCLE, caption="Red Circle with internal dimensions.")
st.image(SVG_RED_CIRCLE, width=300, caption="Red Circle with width 300.")


SVG_YELLOW_GREEN_RECTANGLE = """
<svg viewBox="{x} 0 100 90" xmlns="http://www.w3.org/2000/svg">
    <rect x="0" y="0" width="100" height="90" fill="yellow" />
    <rect x="100" y="0" width="100" height="90" fill="green" />
</svg>
"""

st.image(
    SVG_YELLOW_GREEN_RECTANGLE.format(x=50),
    width=100,
    caption="Yellow Green Rectangle with x 50.",
)
st.image(
    SVG_YELLOW_GREEN_RECTANGLE.format(x=50),
    width=300,
    caption="Yellow Green Rectangle with x 50 and width 300.",
)

st.image(
    SVG_YELLOW_GREEN_RECTANGLE.format(x=0),
    width=100,
    caption="Yellow Green Rectangle with x 0.",
)
st.image(
    SVG_YELLOW_GREEN_RECTANGLE.format(x=0),
    width=300,
    caption="Yellow Green Rectangle with x 0 and width 300.",
)

st.image(
    SVG_YELLOW_GREEN_RECTANGLE.format(x=100),
    width=100,
    caption="Yellow Green Rectangle with x 100.",
)
st.image(
    SVG_YELLOW_GREEN_RECTANGLE.format(x=100),
    width=300,
    caption="Yellow Green Rectangle with x 100 and width 300.",
)

st.header("Image from file")

CAT_IMAGE = os.path.join(TEST_ASSETS_DIR, "cat.jpg")
st.image(CAT_IMAGE, caption="Image from jpg file.", width=200)

st.header("channels parameter")

red_image = Image.new("RGB", (100, 100), color="red")
red_bgr_img = np.array(red_image)[..., ["BGR".index(s) for s in "RGB"]]
st.image(red_bgr_img, caption="BGR channel (red).", channels="BGR", width=100)
st.image(red_bgr_img, caption="RGB channel (blue).", channels="RGB", width=100)

st.header("use_column_width parameter")

col1, col2, col3, col4 = st.columns(4)
col1.image(img)  # 100 px
col1.image(img, use_column_width="auto")  # 100 px
col1.image(img, use_column_width="never")  # 100 px
col1.image(img, use_column_width=False)  # 100 px

col2.image(img, use_column_width="always")  # column width
col2.image(img, use_column_width=True)  # column width
col2.image(img800, use_column_width="auto")  # column width

st.header("List of images")

st.image(
    [
        Image.new("RGB", (64, 64), color="red"),
        Image.new("RGB", (64, 64), color="blue"),
        Image.new("RGB", (64, 64), color="green"),
    ],
    caption=[f"Image list {i}" for i in range(3)],
)
