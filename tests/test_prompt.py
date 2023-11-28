"""Test prompt.py example"""

from prompt import prompt

from clirunner import CliRunner


def test_prompts():
    runner = CliRunner()
    result = runner.invoke(prompt, input="wau wau\n")
    assert not result.exception
    # note: unlike click.CliRunner, clirunner.CliRunner does not echo the input
    assert "foo = wau wau\n" in result.output
