# mbox_converter Configuration Documentation

This document describes all available configuration options for the mbox_converter tool.

## Configuration Parameters

### `sent_from`

**Description:** Include 'From' field

**Type:** `str`

**Default:** `'ON'`

**Choices:** `ON`, `OFF`

**CLI Argument:** `--sent_from`

---

### `to`

**Description:** Include 'To' field

**Type:** `str`

**Default:** `'ON'`

**Choices:** `ON`, `OFF`

**CLI Argument:** `--to`

---

### `date`

**Description:** Include 'Date' field

**Type:** `str`

**Default:** `'ON'`

**Choices:** `ON`, `OFF`

**CLI Argument:** `--date`

---

### `subject`

**Description:** Include 'Subject' field

**Type:** `str`

**Default:** `'ON'`

**Choices:** `ON`, `OFF`

**CLI Argument:** `--subject`

---

### `format`

**Description:** Output format: txt or csv

**Type:** `str`

**Default:** `'txt'`

**Choices:** `txt`, `csv`

**CLI Argument:** `--format`

---

### `max_days`

**Description:** Max number of days per output file (-1 for unlimited)

**Type:** `int`

**Default:** `-1`

**CLI Argument:** `--max_days`

---

### `mbox_file`

**Description:** Path to mbox file

**Type:** `str`

**Default:** `''`

**Required:** Yes

**CLI Argument:** `--mbox_file`

---

## Usage Examples

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
