"""Command-line interface for xldump.

This module provides the CLI entry point and argument parsing for xldump.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from xldump.core import XlDumpError, dump, scan
from xldump.formatters import JsonFormatter


def main() -> int:
    """Run the xldump CLI.

    Returns:
        Exit code (0 for success, non-zero for errors).

    """
    parser = argparse.ArgumentParser(
        prog="xldump",
        description="Dump Excel (.xlsx) physical structure to JSON",
    )

    # Add version
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- scan subcommand ---
    scan_parser = subparsers.add_parser(
        "scan",
        help="List sheets with summary info",
        description="Scan a workbook and list all sheets with summary information.",
    )
    scan_parser.add_argument(
        "file",
        type=Path,
        help="Path to .xlsx file",
    )
    scan_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file (default: stdout)",
    )
    scan_parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indent level (default: 2)",
    )
    scan_parser.add_argument(
        "--compact",
        action="store_true",
        help="Compact JSON output (no indentation)",
    )

    # --- dump subcommand ---
    dump_parser = subparsers.add_parser(
        "dump",
        help="Dump sheet structure to JSON",
        description="Dump the physical structure of Excel sheets to JSON.",
    )
    dump_parser.add_argument(
        "file",
        type=Path,
        help="Path to .xlsx file",
    )
    dump_parser.add_argument(
        "-s",
        "--sheets",
        nargs="+",
        help="Sheet names to dump (default: all)",
    )
    dump_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file (default: stdout)",
    )
    dump_parser.add_argument(
        "--no-styles",
        action="store_true",
        help="Exclude style information",
    )
    dump_parser.add_argument(
        "--no-values",
        action="store_true",
        help="Exclude cell values (style-only mode)",
    )
    dump_parser.add_argument(
        "--no-merges",
        action="store_true",
        help="Exclude merged cell information",
    )
    dump_parser.add_argument(
        "--no-borders",
        action="store_true",
        help="Exclude border information",
    )
    dump_parser.add_argument(
        "--no-validations",
        action="store_true",
        help="Exclude data validation rules",
    )
    dump_parser.add_argument(
        "--no-images",
        action="store_true",
        help="Exclude image position information",
    )
    dump_parser.add_argument(
        "--data-only",
        action="store_true",
        help="Use cached formula results instead of formulas",
    )
    dump_parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indent level (default: 2)",
    )
    dump_parser.add_argument(
        "--compact",
        action="store_true",
        help="Compact JSON output (no indentation)",
    )

    args = parser.parse_args()

    try:
        if args.command == "scan":
            return _run_scan(args)
        elif args.command == "dump":
            return _run_dump(args)
        else:
            parser.print_help()
            return 1
    except XlDumpError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


def _run_scan(args: argparse.Namespace) -> int:
    """Run the scan command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code.

    """
    result = scan(args.file)

    indent = None if args.compact else args.indent
    formatter = JsonFormatter(indent=indent)
    output = formatter.format(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Output written to: {args.output}")
    else:
        print(output)

    return 0


def _run_dump(args: argparse.Namespace) -> int:
    """Run the dump command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code.

    """
    result = dump(
        args.file,
        sheets=args.sheets,
        include_styles=not args.no_styles,
        include_values=not args.no_values,
        include_merges=not args.no_merges,
        include_borders=not args.no_borders,
        include_validations=not args.no_validations,
        include_images=not args.no_images,
        data_only=args.data_only,
    )

    indent = None if args.compact else args.indent
    formatter = JsonFormatter(indent=indent)
    output = formatter.format(result, include_values=not args.no_values)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Output written to: {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
