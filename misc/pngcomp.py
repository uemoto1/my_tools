#!/usr/bin/env python3
import argparse
import os
import subprocess
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("filelist", nargs="+")
parser.add_argument("--scale", default=0.5**0.5, type=float)
parser.add_argument("--suffix",  default="_mini")
parser.add_argument("--quant", "-q", default=False,  action="store_true")
args = parser.parse_args()

for item in args.filelist:
    print(item)
    img = Image.open(item)
    old_width, old_height = img.width, img.height
    new_width = round(old_width * args.scale)
    new_height = round(old_height * args.scale)
    print(f"{old_width}x{old_height}->{new_width}x{new_height}")
    new_size = (new_width, new_height)

    resized_img = img.resize(new_size, Image.LANCZOS)


    title, ext = os.path.splitext(item)
    new_title = f"{title}{args.suffix}.png"
    print(new_title)
    resized_img.save(new_title)

    if args.quant:
        print("pngquant")
        subprocess.call(["pngquant", new_title, "--force"])
