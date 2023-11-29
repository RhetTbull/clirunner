"""Say hello to the world, shouting if desired."""

import os


def hello():
    """Say hello to the world, shouting if desired."""
    if os.getenv("SHOUT") == "1":
        print("HELLO WORLD!")
    else:
        print("Hello World!")


if __name__ == "__main__":
    hello()
