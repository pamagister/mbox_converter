"""Auto-generated CLI interface for mbox_converter project.

This file was generated from config.py parameter definitions.
Do not modify manually - regenerate using MboxConverterConfig.generate_cli_module()
"""

import argparse
from pathlib import Path

from mbox_converter.base import MboxConverter
from mbox_converter.config import MboxConverterConfig


def parse_arguments():
    """Parse command line arguments with config file support."""
    parser = argparse.ArgumentParser(
        description="Parse mbox file and export to text or CSV.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s mailbox.mbox
  %(prog)s --config config.yaml mailbox.mbox
  %(prog)s --format csv --max-days 30 mailbox.mbox
  %(prog)s --from OFF --subject OFF mailbox.mbox
        """,
    )

    # Config file argument
    parser.add_argument("--config", help="Path to configuration file (JSON or YAML)")

    # Generate arguments from config parameters
    for param in MboxConverterConfig.PARAMETERS:
        if param.name == "mbox_file":
            # Positional argument
            parser.add_argument("mbox_file", help=param.help)
        else:
            # Optional argument
            kwargs = {
                "default": param.default,
                "help": f"{param.help} (default: {param.default})",
            }

            if param.name.endswith("_"):
                kwargs["dest"] = param.name

            if param.choices:
                kwargs["choices"] = param.choices

            if param.type_ == int:
                kwargs["type"] = int

            parser.add_argument(param.cli_arg, **kwargs)

    return parser.parse_args()


def main():
    """Main entry point for the CLI application."""
    args = parse_arguments()

    # Create config object
    try:
        # Load from config file if provided
        config = MboxConverterConfig(config_file=args.config if args.config else None)

        # Override with CLI arguments (only if they differ from defaults)
        for param in MboxConverterConfig.PARAMETERS:
            if hasattr(args, param.name):
                arg_value = getattr(args, param.name)
                # Only override if the CLI argument was explicitly provided
                # (i.e., differs from the parameter's default)
                if arg_value != param.default:
                    setattr(config, param.name, arg_value)

        # Validate required parameters
        if not config.mbox_file:
            print("Error: mbox_file is required")
            return 1

        # Check if mbox file exists
        if not Path(config.mbox_file).exists():
            print(f"Error: mbox file not found: {config.mbox_file}")
            return 1

        # Create and run MboxConverter
        converter = MboxConverter(**config.get_kwargs())
        converter.parse()

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
