#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filelist", nargs="+")
    parser.add_argument("--input", "-i", default="image%03d.png", help="Input filename (default: image%03d.png)")
    parser.add_argument("--output", "-o", default="output.mp4", help="Output filename (default: output.mp4)")
    parser.add_argument("--framerate",  "-r", default=12, type=int)
    args = parser.parse_args()

    subprocess.call([
        "ffmpeg",
        "-framerate", str(args.framerate),
        "-i", args.input,
        "-vcodec",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-vf",
        "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        args.output,
    ])
