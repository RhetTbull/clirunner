"""Test clirunner with pydantic-argparse"""

import pytest

try:
    import pydantic
    import pydantic_argparse
except ImportError:
    pytest.skip("pydantic-argparse not installed", allow_module_level=True)

from clirunner import CliRunner


class Arguments(pydantic.BaseModel):
    # Required Args
    string: str = pydantic.Field(description="a required string")
    integer: int = pydantic.Field(description="a required integer")
    flag: bool = pydantic.Field(description="a required flag")

    # Optional Args
    second_flag: bool = pydantic.Field(False, description="an optional flag")
    third_flag: bool = pydantic.Field(True, description="an optional flag")


def main() -> None:
    # Create Parser and Parse Args
    parser = pydantic_argparse.ArgumentParser(
        model=Arguments,
        prog="Example Program",
        description="Example Description",
        version="0.0.1",
        epilog="Example Epilog",
    )
    args = parser.parse_typed_args()

    # Print Args
    print(args)


def test_pydantic_argparse():
    runner = CliRunner()
    result = runner.invoke(
        main, ["--string", "foo", "--integer", "42", "--flag", "--no-third-flag"]
    )
    assert result.exit_code == 0
    assert (
        result.output
        == "string='foo' integer=42 flag=True second_flag=False third_flag=False\n"
    )
