"""doit build script for clirunner; run with `doit` or `doit list` to see available tasks"""

import pathlib

DOIT_CONFIG = {"default_tasks": ["cog_docs", "build_docs", "tests", "build"]}


def task_cog_docs():
    """Update docs"""
    return {"actions": ["cog -r README.md"]}


def task_build_docs():
    """Build docs"""
    return {
        "actions": [
            "cp README.md docs/index.md",
            "mkdocs build",
        ],
        "file_dep": [
            "README.md",
            "docs/index.md",
            "docs/reference.md",
        ],
    }


def task_build():
    """Build the CLI"""
    return {
        "actions": [
            "rm -rf dist/",
            "rm -rf build/",
            "flit build",
        ],
        "file_dep": [
            "clirunner/__init__.py",
            "clirunner/_compat.py",
            "clirunner/_winconsole.py",
            "clirunner/testing.py",
            "clirunner/utils.py",
            "pyproject.toml",
        ],
    }


def task_tests():
    """Run tests"""
    return {"actions": ["python3 -m pytest tests/"]}


def task_docs_deploy():
    """Deploy docs to GitHub pages"""
    return {
        "actions": [
            "mkdocs gh-deploy",
        ],
        "file_dep": [
            "docs/index.md",
            "docs/reference.md",
        ],
    }
