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
