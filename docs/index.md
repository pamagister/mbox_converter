# Welcome to MBOX Converter

[![Github CI Status](https://github.com/pamagister/mbox_converter/actions/workflows/main.yml/badge.svg)](https://github.com/pamagister/mbox_converter/actions)
[![GitHub release](https://img.shields.io/github/v/release/pamagister/mbox_converter)](https://github.com/pamagister/mbox_converter/releases)
[![Read the Docs](https://readthedocs.org/projects/mbox-gmail-converter/badge/?version=stable)](https://mbox-gmail-converter.readthedocs.io/en/stable/)
[![License](https://img.shields.io/github/license/pamagister/mbox_converter)](https://github.com/pamagister/mbox_converter/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/pamagister/mbox_converter)](https://github.com/pamagister/mbox_converter/issues)
[![PyPI](https://img.shields.io/pypi/v/mbox_converter)](https://pypi.org/project/mbox_converter/)



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
