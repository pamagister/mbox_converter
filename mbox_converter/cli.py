"""CLI interface for mbox_converter project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""

import argparse
from math import inf

from mbox_converter.base import MboxConverter


def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse mbox file and export to text or CSV.")
    parser.add_argument(
        "--from",
        dest="from_",
        default="ON",
        choices=["ON", "OFF"],
        help="Include 'From' field (default: ON)",
    )
    parser.add_argument(
        "--to",
        default="ON",
        choices=["ON", "OFF"],
        help="Include 'To' field (default: ON)",
    )
    parser.add_argument(
        "--date",
        default="ON",
        choices=["ON", "OFF"],
        help="Include 'Date' field (default: ON)",
    )
    parser.add_argument(
        "--subject",
        default="ON",
        choices=["ON", "OFF"],
        help="Include 'Subject' field (default: ON)",
    )
    parser.add_argument(
        "--format",
        default="txt",
        choices=["txt", "csv"],
        help="Output format: txt or csv (default: txt)",
    )
    parser.add_argument(
        "--max_days",
        type=int,
        default=-1,
        help="Max number of days per output file (default: unlimited)",
    )
    parser.add_argument("mbox_file", help="Path to mbox file")
    return parser.parse_args()


def main():
    """
    The main function executes on commands:
    `python -m mbox_converter` and `$ mbox_converter `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    args = parse_arguments()
    parser = MboxConverter(
        mbox_file=args.mbox_file,
        include_from=args.from_ == "ON",
        include_to=args.to == "ON",
        include_date=args.date == "ON",
        include_subject=args.subject == "ON",
        output_format=args.format,
        max_days=args.max_days if args.max_days > 0 else inf,
    )
    parser.parse()


if __name__ == "__main__":
    main()
