"""Central configuration management for mbox_converter project.

This module provides a single source of truth for all configuration parameters.
It can generate config files, CLI modules, and documentation from the parameter definitions.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


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
    is_cli: bool = True

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
            name="to",
            default="ON",
            type_=str,
            choices=["ON", "OFF"],
            help="Include 'To' field",
        ),
        ConfigParameter(
            name="date",
            default="ON",
            type_=str,
            choices=["ON", "OFF"],
            help="Include 'Date' field",
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
        ConfigParameter(
            name="date_format",
            default="%Y-%m-%d",
            type_=str,
            help="Date format to use",
            is_cli=False,
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
                import yaml

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
                import yaml

                yaml.dump(config_data, f, default_flow_style=False, indent=2)
            else:
                json.dump(config_data, f, indent=2)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {param.name: getattr(self, param.name) for param in self.PARAMETERS}

    @classmethod
    def generate_cli_markdown_doc(cls, output_file: str):
        """Generate a Markdown CLI documentation with a formatted table and examples."""
        from textwrap import dedent

        rows = []
        required_params = []
        optional_params = []

        for param in cls.PARAMETERS:
            if not param.is_cli:
                continue
            cli_arg = f"`--{param.name}`" if param.name != "mbox_file" else "`path/to/file.mbox`"
            typ = param.type_.__name__
            desc = param.help
            default = (
                "*required*"
                if getattr(param, "required", False) or param.default in (None, "")
                else repr(param.default)
            )
            choices = ", ".join(param.choices) if param.choices else "-"

            rows.append((cli_arg, typ, desc, default, choices))
            if default == "*required*":
                required_params.append(param)
            else:
                optional_params.append(param)

        # Dynamisch Spaltenbreite bestimmen
        def pad(s, width):
            return s + " " * (width - len(s))

        widths = [max(len(str(col)) for col in column) for column in zip(*rows)]
        header = ["Option", "Typ", "Description", "Default", "Choices"]

        # Markdown-Tabelle erstellen
        table = (
            "| "
            + " | ".join(pad(h, w) for h, w in zip(header, widths))
            + " |\n"
            + "|-"
            + "-|-".join("-" * w for w in widths)
            + "-|\n"
        )
        for row in rows:
            table += "| " + " | ".join(pad(str(col), w) for col, w in zip(row, widths)) + " |\n"

        # Beispielbefehle erzeugen
        examples = []
        required_arg = required_params[0].name if required_params else "example.mbox"
        examples.append(
            dedent(
                f"""
        ### 1. Standard version (only required parameter)

        ```bash
        python -m mbox_converter.cli {required_arg}
        ```
        """
            )
        )

        for i in range(1, min(5, len(optional_params) + 1)):
            selected = optional_params[:i]
            cli_part = " ".join(
                f"--{p.name} {p.choices[0] if p.choices else p.default}" for p in selected
            )
            examples.append(
                dedent(
                    f"""
            ### {i + 1}. Example with {i} Parameter(s)

            ```bash
            python -m mbox_converter.cli {cli_part} {required_arg}
            ```
            """
                )
            )

        markdown = dedent(
            """
        # Command line interface

        Command line options

        ```bash
        python -m mbox_converter.cli [OPTIONS] path/to/file.mbox
        ```

        ---

        ## ⚙️ CLI-Options

        {}

        ## 💡 Examples

        In the example, the following is assumed: `example.mbox` in the current directory

        {}
        """
        ).format(table, "".join(examples))

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown.strip())

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
                docs += "**Required:** Yes\n\n"
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
    """Main function to generate config file and documentation."""

    default_config: str = "../config.yaml"
    default_doc: str = "../docs/usage/cli_api_doc.md"

    MboxConverterConfig.generate_default_config_file(default_config)
    print(f"Generated: {default_config}")

    # MboxConverterConfig.generate_markdown_docs(default_doc)
    MboxConverterConfig.generate_cli_markdown_doc(default_doc)
    print(f"Generated: {default_doc}")


if __name__ == "__main__":
    main()
