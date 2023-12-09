"""Test clirunner with Click; this is just to show that it works, you should use click.testing.CliRunner if using Click """

import sys

import instld
import pytest

from clirunner import CliRunner

if sys.platform == "win32":
    pytest.skip(reason="instld does not run on windows CI", allow_module_level=True)


def test_click():
    """Test that clirunner works with Click"""

    with instld("click==8.1.7") as context:
        click = context.import_here("click")

        @click.command()
        @click.option("--count", default=1, help="Number of greetings.")
        @click.option("--name", prompt="Your name", help="The person to greet.")
        def hello(count, name):
            """Simple program that greets NAME for a total of COUNT times."""
            for _ in range(count):
                click.echo(f"Hello, {name}!")

        runner = CliRunner()
        result = runner.invoke(hello, ["--count", "3", "--name", "Jane"])
        assert not result.exception
        assert result.output == "Hello, Jane!\n" * 3
        assert result.exit_code == 0
