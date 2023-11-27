"""Test config for clirunner"""

import pytest

from clirunner import CliRunner


@pytest.fixture(scope="function")
def runner(request):
    return CliRunner()
