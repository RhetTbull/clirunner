"""Simple cat program for testing isolated file system"""

import argparse


def cat():
    argp = argparse.ArgumentParser()
    argp.add_argument("file", type=argparse.FileType("r"))
    args = argp.parse_args()
    print(args.file.read(), end="")


if __name__ == "__main__":
    cat()
