# Welcome to MBOX Converter

**Mbox Converter** is a lightweight, Python-based command-line and GUI tool 
for converting and processing `.mbox` email archive files. 
It supports a variety of output formats and filtering options, 
making it ideal for email analysis, data extraction, and archival purposes.

## Features

* Convert `.mbox` files to structured formats like `.csv` or plain text
* Filter emails by date, sender, subject, and more
* Fast, cross-platform, and fully open-source
* Easy to install via [Poetry](https://python-poetry.org/) or `pip`
* Well-tested with continuous integration across Linux, macOS, and Windows

## Getting Started

To get started, install the tool using:

```bash
poetry install
```

or run it directly with:

```bash
poetry run mbox-converter input.mbox --output-format csv
```

