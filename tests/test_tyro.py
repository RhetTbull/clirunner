"""Test clirunner with tyro"""

from dataclasses import dataclass

import pytest

from clirunner import CliRunner

try:
    import tyro
except ImportError:
    pytest.skip("tyro not installed", allow_module_level=True)


def cli_function():
    def add(a: int, b: int = 3) -> int:
        return a + b

    # Populate the inputs of add(), call it, then return the output.
    total = tyro.cli(add)

    print(total)


def cli_dataclass():
    @dataclass
    class Args:
        a: int
        b: int = 3

    args = tyro.cli(Args)
    print(args.a + args.b)


def test_cli_function():
    runner = CliRunner()
    result = runner.invoke(cli_function, ["--a", "1", "--b", "2"])
    assert not result.exception
    assert result.output == "3\n"

    result = runner.invoke(cli_function, ["--a", "1"])
    assert not result.exception
    assert result.output == "4\n"


def test_cli_dataclass():
    runner = CliRunner()
    result = runner.invoke(cli_dataclass, ["--a", "1", "--b", "2"])
    assert not result.exception
    assert result.output == "3\n"

    result = runner.invoke(cli_dataclass, ["--a", "1"])
    assert not result.exception
    assert result.output == "4\n"
