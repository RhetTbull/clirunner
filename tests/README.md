# Test Files for CliRunner

Run tests with `pytest`

## Tests for Specific Frameworks

The `tests/` directory contains tests for specific frameworks in addition to the regular `argparse` tests. These tests will only be run if the framework is installed. For example,to test `pydantic-argparse`, run `pip install pydantic-argparse` and then run `pytest tests/test_pydantic_argparse.py`.

There are specific tests for the following frameworks:

- [pydantic-argparse](https://pydantic-argparse.supimdos.com/)
- [tyro](https://brentyi.github.io/tyro/)
- [clipstick](https://github.com/sander76/clipstick)
