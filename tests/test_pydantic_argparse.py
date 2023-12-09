"""Test clirunner with pydantic-argparse"""

import sys

import instld
import pytest

from clirunner import CliRunner

if sys.platform == "win32":
    pytest.skip(reason="instld does not run on windows CI", allow_module_level=True)


def test_pydantic_argparse():
    with instld("pydantic-argparse==0.8.0", "pydantic==1.9.0") as context:
        pydantic = context.import_here("pydantic")
        pydantic_argparse = context.import_here("pydantic_argparse")

        class Arguments(pydantic.BaseModel):  # type: ignore
            # Required Args
            string: str = pydantic.Field(description="a required string")  # type: ignore
            integer: int = pydantic.Field(description="a required integer")  # type: ignore
            flag: bool = pydantic.Field(description="a required flag")  # type: ignore

            # Optional Args
            second_flag: bool = pydantic.Field(False, description="an optional flag")  # type: ignore
            third_flag: bool = pydantic.Field(True, description="an optional flag")  # type: ignore

        def main() -> None:
            # Create Parser and Parse Args
            parser = pydantic_argparse.ArgumentParser(  # type: ignore
                model=Arguments,
                prog="Example Program",
                description="Example Description",
                version="0.0.1",
                epilog="Example Epilog",
            )
            args = parser.parse_typed_args()

            # Print Args
            print(args)

        runner = CliRunner()
        result = runner.invoke(
            main, ["--string", "foo", "--integer", "42", "--flag", "--no-third-flag"]
        )
        assert result.exit_code == 0
        assert (
            result.output
            == "string='foo' integer=42 flag=True second_flag=False third_flag=False\n"
        )
