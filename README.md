<!-- This README.md is auto-generated from docs/index.md -->

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
* Easy to install via [uv](https://docs.astral.sh/uv/) or `pip`
* Well-tested with continuous integration across Linux, macOS, and Windows

## Installation


### 🐍 Install from PyPI 

```bash
python -m pip install mbox_converter
```


### 🔽 Download installer

- [⬇️ Download for Windows](https://github.com/pamagister/mbox_converter/releases/latest/download/MboxConverter-win.zip)
- [⬇️ Download for macOS](https://github.com/pamagister/mbox_converter/releases/latest/download/MboxConverter-macOS.zip)


### Run from source

```bash
python -m mbox_converter --format csv example.mbox
```

### Run GUI from source

```bash
python -m mbox_converter.gui
```


### Run command line from source

Creating virtual environment using [uv](https://docs.astral.sh/uv/):
```bash
uv venv
```

Activating a Python virtual environment (`venv`)
> Note: Replace `.venv` with your Venv folder name if you have chosen a different one.

🔹 Windows (PowerShell)

```powershell
.venv\Scripts\activate.ps1
```

🔹 Windows (CMD)
```cmd
.venv\Scripts\activate.bat
```

🔹 Linux / macOS (Bash/Zsh)
```bash
source .venv/bin/activate
```

Run mbox_converter from command line:
```bash
mbox_converter --format csv example.mbox
```

### Run GUI

```bash
mbox_gui
```