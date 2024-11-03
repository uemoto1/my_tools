#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess

def run(file_input, file_output, setting):
    subprocess.call([
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/%s" % setting,
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        "-sOutputFile=%s" % file_output,
        file_input,
    ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filelist", nargs="+")
    parser.add_argument("--setting", default="screen", help="screen | ebook")
    parser.add_argument("--suffix",  default="_min")
    args = parser.parse_args()

    for file_input in args.filelist:
        if os.path.isfile(file_input):
            name, ext = os.path.splitext(file_input)
            file_output = "%s%s.pdf" % (name, args.suffix)
            run(file_input, file_output, args.setting)
        else:
            sys.stderr.write(f"ERROR: {file_input} is not found!\n")
