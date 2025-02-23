#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess

def run1(file_input, file_output, dpi):
    subprocess.call([
        "gs",
        f"-sDEVICE=pdfwrite",
        f"-dCompatibilityLevel=1.4",
        f"-dNOPAUSE",
        f"-dBATCH",
        f"-dSAFER",
        f"-dDownsampleColorImages=true",
        f"-dColorImageDownsampleType=/Bicubic",
        f"-dColorImageResolution={dpi}",
        f"-dColorImageDownsampleThreshold=1.0",
        f"-dDownsampleGrayImages=true",
        f"-dGrayImageDownsampleType=/Bicubic",
        f"-dGrayImageResolution={dpi}",
        f"-dGrayImageDownsampleThreshold=1.0",
        f"-dDownsampleMonoImages=true",
        f"-dMonoImageDownsampleType=/Bicubic",
        f"-dMonoImageResolution={dpi}",
        f"-dMonoImageDownsampleThreshold=1.0",
        f"-sOutputFile={file_output}",
        file_input
    ])

def run2(file_input, file_output, setting):
    subprocess.call([
        f"gs",
        f"-sDEVICE=pdfwrite",
        f"-dCompatibilityLevel=1.4",
        f"-dNOPAUSE",
        f"-dBATCH",
        f"-dSAFER",
        f"-dPDFSETTINGS=/{setting}",
        f"-sOutputFile={file_output}",
        file_input,
    ])



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filelist", nargs="+")
    parser.add_argument("-d", "--density", default=96, type=int, help="Default 96 dpi")
    parser.add_argument("-s", "--setting", default="", help="screen (72dpi) | ebook (150dpi) | printer (300dpi)")
    parser.add_argument("--suffix",  default="_min")
    args = parser.parse_args()

    for file_input in args.filelist:
        if os.path.isfile(file_input):
            name, ext = os.path.splitext(file_input)
            file_output = "%s%s.pdf" % (name, args.suffix)
            if not args.setting:
                run1(file_input, file_output, args.density)
            else:
                run2(file_input, file_output, args.setting)
        else:
            sys.stderr.write(f"ERROR: {file_input} is not found!\n")
