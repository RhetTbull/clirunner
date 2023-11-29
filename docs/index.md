# CliRunner

A test helper for invoking and testing command line interfaces (CLIs). This is adapted from the [Click](https://click.palletsprojects.com/) [CliRunner](https://click.palletsprojects.com/en/8.1.x/testing/) but modified to work with non-Click scripts, such as those using [argparse](https://docs.python.org/3/library/argparse.html) for parsing command line arguments.

## Installation

`python3 -m pip install clirunner`

## Source Code

The source code is available on [GitHub](https://github.com/RhetTbull/clirunner).

## Motivation

I write a lot of Python command line tools. I usually reach for Click to build the CLI but sometimes will use argparse or even just manual `sys.argv` parsing for simple scripts or where I do not want to introduce a dependency on Click. Click provides a very useful [CliRunner](https://click.palletsprojects.com/en/8.1.x/testing/) for testing CLIs, but it only works with Click applications. This project is a derivative of Click's CliRunner that works with non-Click scripts. The API is the same as Click's CliRunner, so it should be easy to switch between the two if you later refactor to use Click.

## Supported Platforms

Tested on macOS, Ubuntu Linux, and Windows using "*-latest" GitHub Workflow runners with Python 3.9 - 3.12.

## Documentation

Full documentation is available [here](https://rhettbull.github.io/clirunner/).

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

from hello import hello

from clirunner import CliRunner


def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(hello, ["--name", "Peter"])
    assert result.exit_code == 0
    assert result.output == "Hello Peter!\n"
```
<!--[[[end]]]-->

Note that `result.output` will contain the combined output of `stdout` and `stderr`. If you want to capture `stdout` and `stderr` separately, use `result.stdout` and `result.stderr`.

## File System Isolation

For basic command line tools with file system operations, the `CliRunner.isolated_filesystem()` method is useful for setting the current working directory to a new, empty folder.

### cat.py

<!--[[[cog
cog.out("\n```python\n")
with open("tests/cat.py", "r") as f:
    cog.out(f.read())
cog.out("```\n")
]]]-->

```python
"""Simple cat program for testing isolated file system"""

import argparse


def cat():
    argp = argparse.ArgumentParser()
    argp.add_argument("file", type=argparse.FileType("r"))
    args = argp.parse_args()
    print(args.file.read(), end="")


if __name__ == "__main__":
    cat()
```
<!--[[[end]]]-->

### test_cat.py

<!--[[[cog
cog.out("\n```python\n")
with open("tests/test_cat.py", "r") as f:
    cog.out(f.read())
cog.out("```\n")
]]]-->

```python
"""Test cat.py example."""

from cat import cat

from clirunner import CliRunner


def test_cat():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("hello.txt", "w") as f:
            f.write("Hello World!\n")

        result = runner.invoke(cat, ["hello.txt"])
        assert result.exit_code == 0
        assert result.output == "Hello World!\n"
```
<!--[[[end]]]-->

Pass `temp_dir` to control where the temporary directory is created. The directory will not be removed by `CliRunner` in this case. This is useful to integrate with a framework like Pytest that manages temporary files.

```python
def test_keep_dir(tmp_path):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        ...
```

## Input Streams

The test wrapper can also be used to provide input data for the input stream (stdin). This is very useful for testing prompts, for instance:

### prompt.py

<!--[[[cog
cog.out("\n```python\n")
with open("tests/prompt.py", "r") as f:
    cog.out(f.read())
cog.out("```\n")
]]]-->

```python
"""Simple example for testing input streams"""


def prompt():
    foo = input("Foo: ")
    print(f"foo = {foo}")


if __name__ == "__main__":
    prompt()
```
<!--[[[end]]]-->

### test_prompt.py

<!--[[[cog
cog.out("\n```python\n")
with open("tests/test_prompt.py", "r") as f:
    cog.out(f.read())
cog.out("```\n")
]]]-->

```python
"""Test prompt.py example"""

from prompt import prompt

from clirunner import CliRunner


def test_prompts():
    runner = CliRunner()
    result = runner.invoke(prompt, input="wau wau\n")
    assert not result.exception
    # note: unlike click.CliRunner, clirunner.CliRunner does not echo the input
    assert "foo = wau wau\n" in result.output
```
<!--[[[end]]]-->

Note that the input will not be echoed to the output stream. This is different from the behavior of the `input()` function, which does echo the input and from click's `prompt()` function, which also echo's the input when under test.

## Environment Variable Isolation

The `CliRunner.invoke()` method can also be used to set environment variables for the command line script. This is useful for testing command line tools that use environment variables for configuration.

### hello_env.py

<!--[[[cog
cog.out("\n```python\n")
with open("tests/hello_env.py", "r") as f:
    cog.out(f.read())
cog.out("```\n")
]]]-->

```python
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
```
<!--[[[end]]]-->

### test_hello_env.py

<!--[[[cog
cog.out("\n```python\n")
with open("tests/test_hello_env.py", "r") as f:
    cog.out(f.read())
cog.out("```\n")
]]]-->

```python
"""Test hello2.py showing how to set environment variables for testing."""

from hello_env import hello

from clirunner import CliRunner


def test_hello():
    """Test hello2.py"""
    runner = CliRunner()
    result = runner.invoke(hello)
    assert result.exit_code == 0
    assert result.output == "Hello World!\n"


def test_hello_shouting():
    """Test hello2.py"""
    runner = CliRunner()
    result = runner.invoke(hello, env={"SHOUT": "1"})
    assert result.exit_code == 0
    assert result.output == "HELLO WORLD!\n"
```
<!--[[[end]]]-->

## Handling Exceptions

Normally the `CliRunner.invoke()` method will catch exceptions in the CLI under test. If an exception is raised, it will be available via the `Result.exception` property. This can be disabled by passing `catch_exceptions=False` to the `CliRunner.invoke()` method.

### raise_exception.py

<!--[[[cog
cog.out("\n```python\n")
with open("tests/raise_exception.py", "r") as f:
    cog.out(f.read())
cog.out("```\n")
]]]-->

```python
"""Simple script that raises an exception"""


def raise_exception():
    """Raises a ValueError exception"""
    raise ValueError("Exception raised")


if __name__ == "__main__":
    raise_exception()
```
<!--[[[end]]]-->

### test_raise_exception.py

<!--[[[cog
cog.out("\n```python\n")
with open("tests/test_raise_exception.py", "r") as f:
    cog.out(f.read())
cog.out("```\n")
]]]-->

```python
"""Test raise_exception.py"""

import pytest
from raise_exception import raise_exception

from clirunner import CliRunner


def test_exception_caught():
    """CliRunner normally catches exceptions"""
    runner = CliRunner()
    result = runner.invoke(raise_exception)
    # exit code will not be 0 if exception is raised
    assert result.exit_code != 0
    assert isinstance(result.exception, ValueError)


def test_exception_not_caught():
    """CliRunner can be configured to not catch exceptions"""
    runner = CliRunner()
    with pytest.raises(ValueError):
        runner.invoke(raise_exception, catch_exceptions=False)
```
<!--[[[end]]]-->

## Testing Click Applications

Do not use `clirunner.CliRunner` to test applications built with [Click](https://pypi.org/project/click/), [Typer](https://pypi.org/project/typer/), or another Click derivative. Instead, use Click's built-in [CliRunner](https://click.palletsprojects.com/en/8.1.x/testing). `clirunner.CliRunner` is only for testing non-Click scripts such as those using [argparse](https://docs.python.org/3/library/argparse.html) or manual [sys.argv](https://docs.python.org/3/library/sys.html#sys.argv) argument parsing.

## License

CliRunner is a derivative work of Click's CliRunner, and so it is licensed under the same BSD 3-clause license as Click. See the [LICENSE](https://github.com/RhetTbull/clirunner/blob/main/LICENSE) file for details.
