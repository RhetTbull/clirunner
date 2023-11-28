"""Test hello.py"""

from hello import hello

from clirunner import CliRunner


def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(hello, ["--name", "Peter"])
    assert result.exit_code == 0
    assert result.output == "Hello Peter!\n"
