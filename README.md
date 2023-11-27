# CliRunner

A test helper for invoking and testing command line interfaces (CLIs). This is adapted from the [Click](https://click.palletsprojects.com/) [CliRunner](https://click.palletsprojects.com/en/8.1.x/testing/) but modified to work with non-Click scripts, such as those using [argparse](https://docs.python.org/3/library/argparse.html) for parsing command line arguments.

## Installation

TODO: not yet on PyPI

## Basic Testing

CliRunner can invoke your CLI's main function as a command line script. The CliRunner.invoke() method runs the command line script in isolation and captures the output as both bytes and binary data.

The return value is a Result object, which has the captured output data, exit code, and optional exception attached:

### hello.py

<!--[[[cog
cog.out("\n```python\n")
with open("tests/hello.py", "r") as f:
    cog.out(f.read())
cog.out("```\n")
]]]-->

```python
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
```
<!--[[[end]]]-->

### test_hello.py

<!--[[[cog
cog.out("\n```python\n")
with open("tests/test_hello.py", "r") as f:
    cog.out(f.read())
cog.out("```\n")
]]]-->

```python
"""Test hello.py"""

from clirunner import CliRunner
from hello import hello


def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(hello, ["--name", "Peter"])
    assert result.exit_code == 0
    assert result.output == "Hello Peter!\n"
```
<!--[[[end]]]-->

## License

CliRunner is a derivative work of Click's CliRunner, and so it is licensed under the same BSD 3-clause license as Click. See the LICENSE file for details.
