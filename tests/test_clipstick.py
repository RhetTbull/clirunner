"""Test clirunner with clipstick; you must install clipstick to run this test."""

import pytest

from clirunner import CliRunner

try:
    from clipstick import parse
    from pydantic import BaseModel
except ImportError:
    pytest.skip("clipstick not installed", allow_module_level=True)


class SimpleModel(BaseModel):
    """A simple model demonstrating clipstick.

    This is used in help as describing the main command.
    """

    name: str
    """Your name. This is used in help describing name."""

    repeat_count: int = 10
    """How many times to repeat your name. Used in help describing repeat_count."""

    def main(self):
        for _ in range(self.repeat_count):
            print(f"hello: {self.name}")


def cli():
    model = parse(SimpleModel)
    model.main()


def test_clipstick():
    runner = CliRunner()
    result = runner.invoke(cli, ["world", "--repeat-count", "10"])
    assert result.output == "hello: world\n" * 10
    assert result.exit_code == 0
