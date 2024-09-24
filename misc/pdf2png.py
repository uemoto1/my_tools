#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess

def run(file_input, file_output, setting, dpi):
    subprocess.call([
        "gs",
        "-sDEVICE=%s" % setting,
        "-r%d" % dpi,
        "-dGraphicsAlphaBits=4",
        "-dTextAlphaBits=4",
        "-o", file_output,
        file_input,
    ])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filelist", nargs="+")
    parser.add_argument("--setting", default="png16m", help="png16m | pnggray | pngalpha")
    parser.add_argument("--dpi", default=144, type=int)
    parser.add_argument("--suffix",  default="_%03d")
    args = parser.parse_args()

    for file_input in args.filelist:
        if os.path.isfile(file_input):
            name, ext = os.path.splitext(file_input)
            file_output = "%s%s.png" % (name, args.suffix)
            sys.stdout.write(f"Convert {file_input} to png\n")
            run(file_input, file_output, args.setting, args.dpi)
        else:
            sys.stderr.write(f"ERROR: {file_input} is not found!\n")
