[![Github CI Status](https://github.com/pamagister/mbox_converter/actions/workflows/main.yml/badge.svg)](https://github.com/pamagister/mbox_converter/actions)
[![GitHub release](https://img.shields.io/github/v/release/pamagister/mbox_converter)](https://github.com/pamagister/mbox_converter/releases)
[![License](https://img.shields.io/github/license/pamagister/mbox_converter)](https://github.com/pamagister/mbox_converter/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/pamagister/mbox_converter)](https://github.com/pamagister/mbox_converter/issues)
[![PyPI](https://img.shields.io/pypi/v/mbox_converter)](https://pypi.org/project/mbox_converter/)



# MBOX Converter

A Python script for parsing and structured export of `.mbox` files.
Supports output in text or CSV format with optional on/off email fields.
Useful for analyzing, archiving or further processing e-mail correspondence.

## 🔽 Download installer

- [⬇️ Download for Windows](https://github.com/pamagister/mbox_converter/releases/latest/download/MboxConverter-win.zip)
- [⬇️ Download for macOS](https://github.com/pamagister/mbox_converter/releases/latest/download/MboxConverter-macOS.zip)


## Run from source code

Setup & execution

### 1. prepare the repository

```bash
# Create virtual environment (optional, recommended)
python -m venv env
source env/bin/activate  # Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

````

### 2. Execute script

```bash
python -m mbox_converter.cli [OPTIONS] path/to/file.mbox
```


## 📁 Output

* **Text mode (`--format txt`)**: Contains structured text blocks with fields and e-mail content.
* **CSV Mode (`--format csv`)**: CSV file with one line per mail. Fields correspond to the activated CLI options.

The output files are numbered automatically:

```bash
example_001.txt
example_002.txt
...
```

---

## 🔚 Exiting the virtual environment

```bash
deactivate
```

Certainly! Here's an additional chapter you can include in your `README.md` file under the title:

---

## 🖱️ Usage by Drag-and-Drop

You can also run the Converter conveniently by dragging and dropping `.mbox` files onto the provided startup scripts. This is especially useful for non-technical users or quick one-off processing.

---

### 🪟 Windows (`.bat` file)

#### File: `DnD_mbox_converter.bat` or `DnD_mbox_converter.bat`

**Steps:**

1. Make sure `mbox_converter.py`, `requirements.txt`, and the `.bat` file are in the same directory.
2. Drag a `.mbox` file and drop it onto the `.bat` file (e.g. `example.mbox`).
3. The script will:

   * create a virtual environment (if not already present),
   * install all dependencies,
   * run the Converter with default options.

> 💡 Output files will be created in the same directory, with names like `example_001.txt` or `example_001.csv`.

---

### 🐧 Linux/macOS (`.sh` file)

#### File: `setup_and_run.sh`

**Steps:**

1. Place `setup_and_run.sh`, `mbox_converter.py`, and `requirements.txt` in the same directory.

2. Make the script executable:

   ```bash
   chmod +x setup_and_run.sh
   ```

3. Open a terminal.

4. Drag your `.mbox` file into the terminal window — it will paste the full path.

5. Complete the command like this:

   ```bash
   ./setup_and_run.sh /full/path/to/example.mbox
   ```

6. The script will:

   * create and activate a `.venv` if needed,
   * install requirements,
   * and run the Converter on the file.

---

### 📝 Notes

* The `.venv` directory will be reused across runs.
* You can modify the batch or shell script to hard-code specific Converter options (like `--format csv`), if desired.

Let me know if you’d like a version that includes GUI elements (e.g., file picker dialogs).



## References

- [Installing packages using pip and virtual environments](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
- A tutorial on working with [Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html)
- [A Guide to Python’s Virtual Environments](https://towardsdatascience.com/virtual-environments-104c62d48c54)
- [MBOX Parsing Example: Mining the Social](https://www.oreilly.com/library/view/mining-the-social/9781449368180/ch06.html)

