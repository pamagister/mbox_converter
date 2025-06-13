"""Central configuration management for mbox_converter project.

This module provides a single source of truth for all configuration parameters.
It can generate config files, CLI modules, and documentation from the parameter definitions.
"""

import json
from dataclasses import dataclass, field
from math import inf
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml


@dataclass
class ConfigParameter:
    """Represents a single configuration parameter with all its metadata."""

    name: str
    default: Any
    type_: type
    choices: Optional[List[str]] = None
    help: str = ""
    cli_arg: Optional[str] = None
    required: bool = False

    def __post_init__(self):
        if self.cli_arg is None:
            self.cli_arg = f"--{self.name}"


class MboxConverterConfig:
    """Central configuration class for mbox_converter.

    All parameters are defined here as class attributes with their metadata.
    This serves as the single source of truth for configuration management.
    """

    # Define all configuration parameters
    PARAMETERS = [
        ConfigParameter(
            name="sent_from",
            default="ON",
            type_=str,
            choices=["ON", "OFF"],
            help="Include 'From' field",
        ),
        ConfigParameter(
            name="to", default="ON", type_=str, choices=["ON", "OFF"], help="Include 'To' field"
        ),
        ConfigParameter(
            name="date", default="ON", type_=str, choices=["ON", "OFF"], help="Include 'Date' field"
        ),
        ConfigParameter(
            name="subject",
            default="ON",
            type_=str,
            choices=["ON", "OFF"],
            help="Include 'Subject' field",
        ),
        ConfigParameter(
            name="format",
            default="txt",
            type_=str,
            choices=["txt", "csv"],
            help="Output format: txt or csv",
        ),
        ConfigParameter(
            name="max_days",
            default=-1,
            type_=int,
            help="Max number of days per output file (-1 for unlimited)",
        ),
        ConfigParameter(
            name="mbox_file",
            default="",
            type_=str,
            help="Path to mbox file",
            required=True,
            cli_arg=None,  # Positional argument
        ),
    ]

    def __init__(self, config_file: Optional[str] = None, **kwargs):
        """Initialize configuration from file and/or keyword arguments.

        Args:
            config_file: Path to configuration file (JSON or YAML)
            **kwargs: Override parameters
        """
        # Set defaults
        for param in self.PARAMETERS:
            setattr(self, param.name, param.default)

        # Load from file if provided
        print(f"### {config_file}")
        if config_file:
            self.load_from_file(config_file)

        # Override with provided kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def load_from_file(self, config_file: str):
        """Load configuration from JSON or YAML file."""
        config_path = Path(config_file)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")

        with open(config_path, "r", encoding="utf-8") as f:
            if config_path.suffix.lower() in [".yml", ".yaml"]:
                config_data = yaml.safe_load(f)
            else:
                config_data = json.load(f)
            print(config_data)

        for key, value in config_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def save_to_file(self, config_file: str, format_: str = "auto"):
        """Save current configuration to file.

        Args:
            config_file: Path to save configuration
            format_: Format to use ('json', 'yaml', or 'auto' to detect from extension)
        """
        config_path = Path(config_file)
        config_data = self.to_dict()

        # Determine format
        if format_ == "auto":
            format_ = "yaml" if config_path.suffix.lower() in [".yml", ".yaml"] else "json"

        # Ensure directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w", encoding="utf-8") as f:
            if format_ == "yaml":
                yaml.dump(config_data, f, default_flow_style=False, indent=2)
            else:
                json.dump(config_data, f, indent=2)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {param.name: getattr(self, param.name) for param in self.PARAMETERS}

    def get_kwargs(self) -> Dict[str, Any]:
        """Get kwargs suitable for MboxConverter constructor."""
        return {
            "mbox_file": self.mbox_file,
            "include_from": self.sent_from == "ON",
            "include_to": self.to == "ON",
            "include_date": self.date == "ON",
            "include_subject": self.subject == "ON",
            "output_format": self.format,
            "max_days": self.max_days if self.max_days > 0 else inf,
        }

    @classmethod
    def generate_default_config_file(cls, output_file: str):
        """Generate a default configuration file with all parameters and their descriptions."""
        config = cls()

        # Add comments to YAML
        config_data = {}
        for param in cls.PARAMETERS:
            config_data[param.name] = {
                "value": param.default,
                "help": param.help,
                "type": param.type_.__name__,
                "choices": param.choices if param.choices else None,
            }

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# mbox_converter Configuration File\n")
            f.write("# This file was auto-generated. Modify as needed.\n\n")

            for param in cls.PARAMETERS:
                f.write(f"# {param.help}\n")
                if param.choices:
                    f.write(f"# Choices: {', '.join(param.choices)}\n")
                f.write(f"# Type: {param.type_.__name__}\n")
                f.write(f"{param.name}: {repr(param.default)}\n\n")

    @classmethod
    def generate_cli_module(cls, output_file: str):
        """Generate CLI module based on parameter definitions."""
        cli_code = '''"""Auto-generated CLI interface for mbox_converter project.

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
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
'''

        # Generate argument definitions
        for param in cls.PARAMETERS:
            if param.name == "mbox_file":
                # Positional argument
                cli_code += f"    parser.add_argument(\n"
                cli_code += f'        "mbox_file",\n'
                cli_code += f'        help="{param.help}"\n'
                cli_code += f"    )\n"
            else:
                # Optional argument
                cli_code += f"    parser.add_argument(\n"
                cli_code += f'        "{param.cli_arg}",\n'
                if param.name.endswith("_"):
                    cli_code += f'        dest="{param.name}",\n'
                cli_code += f"        default={repr(param.default)},\n"
                if param.choices:
                    cli_code += f"        choices={param.choices},\n"
                if param.type_ == int:
                    cli_code += f"        type=int,\n"
                cli_code += f'        help="{param.help} (default: {param.default})"\n'
                cli_code += f"    )\n"

        cli_code += '''
    return parser.parse_args()


def main():
    """Main entry point for the CLI application."""
    args = parse_arguments()
    
    # Create config from CLI arguments
    config = MboxConverterConfig()
    for param in MboxConverterConfig.PARAMETERS:
        if hasattr(args, param.name):
            setattr(config, param.name, getattr(args, param.name))
    
    # Create and run MboxConverter
    converter = MboxConverter(**config.get_kwargs())
    converter.parse()


if __name__ == "__main__":
    main()
'''

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cli_code)

    @classmethod
    def generate_markdown_docs(cls, output_file: str):
        """Generate Markdown documentation for all configuration parameters."""
        docs = """# mbox_converter Configuration Documentation

This document describes all available configuration options for the mbox_converter tool.

## Configuration Parameters

"""

        for param in cls.PARAMETERS:
            docs += f"### `{param.name}`\n\n"
            docs += f"**Description:** {param.help}\n\n"
            docs += f"**Type:** `{param.type_.__name__}`\n\n"
            docs += f"**Default:** `{repr(param.default)}`\n\n"
            if param.choices:
                docs += f"**Choices:** {', '.join(f'`{choice}`' for choice in param.choices)}\n\n"
            if param.required:
                docs += f"**Required:** Yes\n\n"
            if param.cli_arg:
                docs += f"**CLI Argument:** `{param.cli_arg}`\n\n"
            docs += "---\n\n"

        docs += """## Usage Examples

### Using Configuration File

```bash
# Generate default config file
python -c "from mbox_converter.config import MboxConverterConfig; MboxConverterConfig.generate_default_config_file()"

# Use config file
python -m mbox_converter --config mbox_converter_config.yaml
```

### Using CLI Arguments

```bash
# Basic usage
python -m mbox_converter --format csv --max_days 30 /path/to/mailbox.mbox

# Disable certain fields
python -m mbox_converter --sent_from OFF --subject OFF /path/to/mailbox.mbox
```

### Programmatic Usage

```python
from mbox_converter.config import MboxConverterConfig
from mbox_converter.base import MboxConverter

# Create config
config = MboxConverterConfig(
    mbox_file="/path/to/mailbox.mbox",
    format="csv",
    max_days=30
)

# Use with converter
converter = MboxConverter(**config.get_kwargs())
converter.parse()
```
"""

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(docs)


def main():
    """Main function to generate config file, CLI module, and documentation."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python config.py <command>")
        print("Commands:")
        print("  generate-config  - Generate default configuration file")
        print("  generate-cli     - Generate CLI module")
        print("  generate-docs    - Generate Markdown documentation")
        print("  generate-all     - Generate everything")
        return

    command = sys.argv[1]
    default_config: str = "mbox_converter/config.yaml"
    default_doc: str = "docs/usage/cli_api_doc.md"
    default_cli: str = "mbox_converter/cli.py"

    if command == "generate-config" or command == "generate-all":
        MboxConverterConfig.generate_default_config_file(default_config)
        print(f"Generated: {default_config}")

    if command == "generate-cli" or command == "generate-all":
        MboxConverterConfig.generate_cli_module(default_cli)
        print(f"Generated: {default_cli}")

    if command == "generate-docs" or command == "generate-all":
        MboxConverterConfig.generate_markdown_docs(default_doc)
        print(f"Generated: {default_doc}")


if __name__ == "__main__":
    main()
