# Cli legacy

Command line options


```bash
python -m mbox_converter.cli [OPTIONS] path/to/file.mbox
```

---

## ⚙️ CLI-Options

| Option              | Typ        | Description                                                               | Default value  |
| ------------------- |------------|---------------------------------------------------------------------------|----------------|
| `--from`            | `ON/OFF`   | Outputs the sender address                                                | `ON`           |
| `--to`              | `ON/OFF`   | Outputs the recipient address                                             | `ON`           |
| `--date`            | `ON/OFF`   | Outputs the shipping date                                                 | `ON`           |
| `--subject`         | `ON/OFF`   | Outputs the subject                                                       | `ON`           |
| `--format`          | `txt/csv`  | Defines the output format (text file or CSV file)                         | `txt`          |
| `--max_days`        | Number     | Maximum number of days per output file (e.g. '7' for weekly splits)       | `inf`          |
| `path/to/file.mbox` | File       | Path to the MBOX file to be processed                                     | *required* |



## 💡 Examples

In the example, the following is assumed: `example.mbox` in the current directory

### 1. standard version (all fields, text format)

```bash
python -m mbox_converter.cli example.mbox
```

### 2. sender & subject only, in CSV format

```bash
python -m mbox_converter.cli --to OFF --date OFF --format csv example.mbox
```

### 3. grouping of issues by week (7 days per file)

```bash
python -m mbox_converter.cli --max_days 7 example.mbox
```

### 4. complete control (subject only, CSV, grouped daily)

```bash
python -m mbox_converter.cli --sent_from OFF --to OFF --date OFF --format csv --max_days 1 example.mbox
```

---
