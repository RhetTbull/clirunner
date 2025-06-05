"""Test clirunner with tyro"""

import sys
from dataclasses import dataclass

import instld
import pytest

from clirunner import CliRunner

if sys.platform == "win32":
    pytest.skip(reason="instld does not run on windows CI", allow_module_level=True)


def test_cli_function():
    with instld("tyro") as context:
        tyro = context.import_here("tyro")

        def cli_function():
            def add(a: int, b: int = 3) -> int:
                return a + b

            # Populate the inputs of add(), call it, then return the output.
            total = tyro.cli(add)

            print(total)

        runner = CliRunner()
        result = runner.invoke(cli_function, ["--a", "1", "--b", "2"])
        assert not result.exception
        assert result.output == "3\n"

        result = runner.invoke(cli_function, ["--a", "1"])
        assert not result.exception
        assert result.output == "4\n"


def test_cli_dataclass():
    with instld("tyro>=0.6.0") as context:
        tyro = context.import_here("tyro")

        def cli_dataclass():
            @dataclass
            class Args:
                a: int
                b: int = 3

            args = tyro.cli(Args)
            print(args.a + args.b)

        runner = CliRunner()
        result = runner.invoke(cli_dataclass, ["--a", "1", "--b", "2"])
        assert not result.exception
        assert result.output == "3\n"

        result = runner.invoke(cli_dataclass, ["--a", "1"])
        assert not result.exception
        assert result.output == "4\n"
