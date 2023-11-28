"""Tests for CliRunner"""

import argparse
import os
import sys
from io import BytesIO

import pytest

from clirunner._compat import WIN
from clirunner.testing import CliRunner
from clirunner.utils import get_binary_stream


def test_runner():
    def test():
        i = get_binary_stream("stdin")
        o = get_binary_stream("stdout")
        while True:
            chunk = i.read(4096)
            if not chunk:
                break
            o.write(chunk)
            o.flush()

    runner = CliRunner()
    result = runner.invoke(test, input="Hello World!\n")
    assert not result.exception
    assert result.output == "Hello World!\n"


def test_echo_stdin_stream():
    def test():
        i = get_binary_stream("stdin")
        o = get_binary_stream("stdout")
        while True:
            chunk = i.read(4096)
            if not chunk:
                break
            o.write(chunk)
            o.flush()

    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(test, input="Hello World!\n")
    assert not result.exception
    assert result.output == "Hello World!\nHello World!\n"


def test_echo_stdin_prompts():
    def test_python_input():
        foo = input("Foo: ")
        print(f"foo={foo}")

    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(test_python_input, input="bar bar\n")
    assert not result.exception
    assert result.output == "Foo: bar bar\nfoo=bar bar\n"


def test_runner_with_stream():
    def test():
        i = get_binary_stream("stdin")
        o = get_binary_stream("stdout")
        while True:
            chunk = i.read(4096)
            if not chunk:
                break
            o.write(chunk)
            o.flush()

    runner = CliRunner()
    result = runner.invoke(test, input=BytesIO(b"Hello World!\n"))
    assert not result.exception
    assert result.output == "Hello World!\n"

    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(test, input=BytesIO(b"Hello World!\n"))
    assert not result.exception
    assert result.output == "Hello World!\nHello World!\n"


def test_getchar():
    def continue_it():
        print(sys.stdin.read(1))

    runner = CliRunner()
    result = runner.invoke(continue_it, input="y\n")
    assert not result.exception
    assert result.output == "y\n"


def test_catch_exceptions():
    class CustomError(Exception):
        pass

    def cli():
        raise CustomError(1)

    runner = CliRunner()

    result = runner.invoke(cli)
    assert isinstance(result.exception, CustomError)
    assert type(result.exc_info) is tuple
    assert len(result.exc_info) == 3

    with pytest.raises(CustomError):
        runner.invoke(cli, catch_exceptions=False)

    CustomError = SystemExit

    result = runner.invoke(cli)
    assert result.exit_code == 1


def test_exit_code_and_output_from_sys_exit():
    # See issue #362
    def cli_string():
        print("hello world")
        sys.exit("error")

    def cli_int():
        print("hello world")
        sys.exit(1)

    def cli_float():
        print("hello world")
        sys.exit(1.0)

    def cli_no_error():
        print("hello world")

    runner = CliRunner()

    result = runner.invoke(cli_string)
    assert result.exit_code == 1
    assert result.output == "hello world\nerror\n"

    result = runner.invoke(cli_int)
    assert result.exit_code == 1
    assert result.output == "hello world\n"

    result = runner.invoke(cli_float)
    assert result.exit_code == 1
    assert result.output == "hello world\n1.0\n"

    result = runner.invoke(cli_no_error)
    assert result.exit_code == 0
    assert result.output == "hello world\n"


def test_env():
    def cli_env():
        print(f"ENV={os.environ['TEST_CLICK_ENV']}")

    runner = CliRunner()

    env_orig = dict(os.environ)
    env = dict(env_orig)
    assert "TEST_CLICK_ENV" not in env
    env["TEST_CLICK_ENV"] = "some_value"
    result = runner.invoke(cli_env, env=env)
    assert result.exit_code == 0
    assert result.output == "ENV=some_value\n"

    assert os.environ == env_orig


def test_output():
    def cli_output():
        print("stdout")
        print("sys.stdout", file=sys.stdout)
        print("sys.stderr", file=sys.stderr)

    runner = CliRunner()
    result = runner.invoke(cli_output)

    assert result.output == "stdout\nsys.stdout\nsys.stderr\n"


def test_stderr():
    def cli_stderr():
        print("stdout")
        print("stderr", file=sys.stderr)

    runner = CliRunner()

    result = runner.invoke(cli_stderr)

    assert result.output == "stdout\nstderr\n"
    assert result.stdout == "stdout\n"
    assert result.stderr == "stderr\n"


@pytest.mark.parametrize(
    "args, expected_output",
    [
        (None, "bar\n"),
        ([], "bar\n"),
        ("", "bar\n"),
        (["--foo", "one two"], "one two\n"),
        ('--foo "one two"', "one two\n"),
    ],
)
def test_args(args, expected_output):
    def cli_args(*args, **kwargs):
        argparser = argparse.ArgumentParser()
        argparser.add_argument("--foo", default="bar", required=False)
        args = argparser.parse_args()
        print(args.foo)

    runner = CliRunner()
    result = runner.invoke(cli_args, args=args)
    assert result.exit_code == 0
    assert result.output == expected_output


def test_setting_prog_name_in_extra():
    def cli():
        print("ok")

    runner = CliRunner()
    result = runner.invoke(cli, prog_name="foobar")
    assert not result.exception
    assert result.output == "ok\n"


def test_setting_prog_name_in_extra_2():
    def cli():
        print(sys.argv[0])

    runner = CliRunner()
    result = runner.invoke(cli, prog_name="foobar")
    assert not result.exception
    assert result.output == "foobar\n"


def test_command_standalone_mode_returns_value():
    def cli():
        print("ok")
        return "Hello, World!"

    runner = CliRunner()
    result = runner.invoke(cli, standalone_mode=False)
    assert result.output == "ok\n"
    assert result.return_value == "Hello, World!"
    assert result.exit_code == 0


def test_isolated_runner(runner):
    with runner.isolated_filesystem() as d:
        assert os.path.exists(d)

    assert not os.path.exists(d)


def test_isolated_runner_custom_tempdir(runner, tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path) as d:
        assert os.path.exists(d)

    assert os.path.exists(d)
    os.rmdir(d)


def test_isolation_stderr_errors():
    """Writing to stderr should escape invalid characters instead of
    raising a UnicodeEncodeError.
    """

    def cli_stderr():
        sys.stderr.write("\udce2")

    runner = CliRunner()

    result = runner.invoke(cli_stderr)
    assert result.exit_code == 0
    assert result.stderr == "\\udce2"
