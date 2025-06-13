# Command line interface

Command line options

```bash
python -m mbox_converter.cli [OPTIONS] path/to/file.mbox
```

---

## ⚙️ CLI-Options

| Option              | Typ | Description                                           | Default    | Choices  |
|---------------------|-----|-------------------------------------------------------|------------|----------|
| `--sent_from`       | str | Include 'From' field                                  | 'ON'       | ON, OFF  |
| `--to`              | str | Include 'To' field                                    | 'ON'       | ON, OFF  |
| `--date`            | str | Include 'Date' field                                  | 'ON'       | ON, OFF  |
| `--subject`         | str | Include 'Subject' field                               | 'ON'       | ON, OFF  |
| `--format`          | str | Output format: txt or csv                             | 'txt'      | txt, csv |
| `--max_days`        | int | Max number of days per output file (-1 for unlimited) | -1         | -        |
| `path/to/file.mbox` | str | Path to mbox file                                     | *required* | -        |


## 💡 Examples

In the example, the following is assumed: `example.mbox` in the current directory


### 1. Standard version (only required parameter)

```bash
python -m mbox_converter.cli mbox_file
```

### 2. Example with 1 Parameter(s)

```bash
python -m mbox_converter.cli --sent_from ON mbox_file
```

### 3. Example with 2 Parameter(s)

```bash
python -m mbox_converter.cli --sent_from ON --to ON mbox_file
```

### 4. Example with 3 Parameter(s)

```bash
python -m mbox_converter.cli --sent_from ON --to ON --date ON mbox_file
```

### 5. Example with 4 Parameter(s)

```bash
python -m mbox_converter.cli --sent_from ON --to ON --date ON --subject ON mbox_file
```