"""Test cat.py example."""

from cat import cat

from clirunner import CliRunner


def test_cat():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("hello.txt", "w") as f:
            f.write("Hello World!\n")

        result = runner.invoke(cat, ["hello.txt"])
        assert result.exit_code == 0
        assert result.output == "Hello World!\n"
