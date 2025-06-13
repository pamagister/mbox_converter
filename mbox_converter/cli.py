"""Auto-generated CLI interface for mbox_converter project.

This file was generated from config.py parameter definitions.
Do not modify manually - regenerate using MboxConverterConfig.generate_cli_module()
"""

import argparse
from math import inf
from pathlib import Path

from mbox_converter.base import MboxConverter
from mbox_converter.config import MboxConverterConfig


def parse_arguments():
    """Parse command line arguments based on configuration parameters."""
    parser = argparse.ArgumentParser(
        description="Parse mbox file and export to text or CSV.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--sent_from",
        default="ON",
        choices=["ON", "OFF"],
        help="Include 'From' field (default: ON)",
    )
    parser.add_argument(
        "--to", default="ON", choices=["ON", "OFF"], help="Include 'To' field (default: ON)"
    )
    parser.add_argument(
        "--date", default="ON", choices=["ON", "OFF"], help="Include 'Date' field (default: ON)"
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
        default=-1,
        type=int,
        help="Max number of days per output file (-1 for unlimited) (default: -1)",
    )
    parser.add_argument("mbox_file", help="Path to mbox file")

    return parser.parse_args()


def main():
    """Main entry point for the CLI application."""
    # parser = argparse.ArgumentParser()
    args = parse_arguments()
    print(args)

    # explicit_args = parser.parse_args()

    # Create config from CLI arguments
    config = MboxConverterConfig("config.yaml")
    for param in MboxConverterConfig.PARAMETERS:
        if hasattr(args, param.name):
            print(f"{param.name}: {param.default}, {getattr(args, param.name)}")

    print(config.to_dict())
    # Create and run MboxConverter
    converter = MboxConverter(**config.get_kwargs())
    converter.parse()


if __name__ == "__main__":
    main()
