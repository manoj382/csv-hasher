# CSV-Hasher

## Description

`csv-hasher` is a Python script that hashes a specific column in a CSV file. The hash can be generated using different algorithms, with SHA-224 as the default. The script generates both a full-length hash and a truncated 50-character hash. It also checks for and reports any hash clashes in the truncated hashes.

## Requirements

- Python 3.x
- Pandas library

You can install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Basic usage:

```bash
python csv-hasher.py <input_csv_path> <output_csv_path> <column_to_hash>
```

- `input_csv_path`: The path to the input CSV file.
- `output_csv_path`: The path to save the output CSV file.
- `column_to_hash`: The name of the column you want to hash.

### Advanced usage:

You can specify the hash algorithm using the `-a` or `--algorithm` flag:

```bash
python csv-hasher.py <input_csv_path> <output_csv_path> <column_to_hash> -a <algorithm>
```

- `algorithm`: The hash algorithm to use (e.g., `sha256`, `md5`). Default is `sha224`.

### Example:

```bash
python csv-hasher.py input.csv output.csv column_name -a sha256
```

## Output

- The script will output a new CSV file with two additional columns:
  1. One for the full-length hash (`<column_to_hash>_hash_full`).
  2. One for the truncated 50-character hash (`<column_to_hash>_hash_truncated`).
  
- A message will be printed to indicate if any hash clashes are found in the truncated hash column.
