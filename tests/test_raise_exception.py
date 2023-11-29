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
