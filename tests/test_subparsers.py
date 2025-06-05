"""Test service.py with subparsers using CliRunner."""

from service import main

from clirunner import CliRunner


def test_service_new():
    """Test 'service new' subcommand."""
    runner = CliRunner()
    result = runner.invoke(main, ["new", "--name", "1K-cat", "--dims", "2048, 512"])
    assert result.exit_code == 0
    assert "Creating service: 1K-cat" in result.output
    assert "Dimensions: [2048, 512]" in result.output


def test_service_remove():
    """Test 'service remove' subcommand."""
    runner = CliRunner()
    result = runner.invoke(main, ["remove", "--name", "1K-cat"])
    assert result.exit_code == 0
    assert "Removing service: 1K-cat" in result.output


def test_service_no_subcommand():
    """Test service with no subcommand shows help."""
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 1
    assert "Service management CLI" in result.output


def test_service_new_missing_name():
    """Test 'service new' with missing name argument."""
    runner = CliRunner()
    result = runner.invoke(main, ["new", "--dims", "2048, 512"])
    assert result.exit_code != 0


def test_service_new_missing_dims():
    """Test 'service new' with missing dims argument."""
    runner = CliRunner()
    result = runner.invoke(main, ["new", "--name", "test"])
    assert result.exit_code != 0
