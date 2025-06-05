"""Simple CLI app with subparsers for testing CliRunner."""

import argparse
import sys


def parse_dims(dims_str):
    """Parse dimensions string into list of integers."""
    return [int(x.strip()) for x in dims_str.split(",")]


def cmd_new(args):
    """Handle 'new' subcommand."""
    print(f"Creating service: {args.name}")
    print(f"Dimensions: {args.dims}")
    return 0


def cmd_remove(args):
    """Handle 'remove' subcommand."""
    print(f"Removing service: {args.name}")
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Service management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'new' subcommand
    new_parser = subparsers.add_parser("new", help="Create a new service")
    new_parser.add_argument("--name", type=str, required=True, help="Service name")
    new_parser.add_argument(
        "--dims",
        type=parse_dims,
        required=True,
        help="Dimensions as comma-separated integers",
    )
    new_parser.set_defaults(func=cmd_new)

    # 'remove' subcommand
    remove_parser = subparsers.add_parser("remove", help="Remove a service")
    remove_parser.add_argument("--name", type=str, required=True, help="Service name")
    remove_parser.set_defaults(func=cmd_remove)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
