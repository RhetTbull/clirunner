"""Simple CLI """

import argparse


def hello():
    """Print Hello World"""
    argp = argparse.ArgumentParser(description="Print Hello World")
    argp.add_argument("-n", "--name", help="Name to greet")
    args = argp.parse_args()
    print(f"Hello {args.name or 'World'}!")


if __name__ == "__main__":
    hello()
