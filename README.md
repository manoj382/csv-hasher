# CSV Hasher

## Description
This Python script reads a CSV file, hashes a specified column using a selected hashing algorithm, and then writes the updated data to a new CSV file. Optionally, the hash can be truncated to a specified length, and the script checks for hash clashes if truncation is enabled.

## Requirements
- Python 3.x
- Pandas

Install the required Python packages using `pip install -r requirements.txt`.

## Usage

### Basic Syntax

```bash
python csv-hasher.py input_path output_path col_to_hash [-a ALGORITHM] [-l LENGTH] [-s SALT]
```

### Parameters

- `input_path`: Path to the input CSV file.
- `output_path`: Path where the output CSV file will be saved.
- `col_to_hash`: The name of the column to hash.
- `-a` or `--algorithm`: Optional. Hash algorithm to use. Default is `sha224`.
- `-l` or `--length`: Optional. Length to truncate the hash.
- `-s` or `--salt`: Optional. Salt to add to the hash.


### Examples

1. Hash column 'email' using default SHA224 algorithm.
```bash
python csv-hasher.py input.csv output.csv email
```

2. Hash column 'email' using SHA256 algorithm.
```bash
python csv-hasher.py input.csv output.csv email -a sha256
```

3. Hash and truncate the column 'email' to 50 characters.
```bash
python csv-hasher.py input.csv output.csv email -l 50
```

4. Use SHA256 and truncate to 50 characters.
```bash
python csv-hasher.py input.csv output.csv email -a sha256 -l 50
```

5. Hash column 'email' using SHA256 algorithm and salt 'my_salt'.
```bash
python csv-hasher.py input.csv output.csv email -a sha256 -s my_salt
```

## Output

- The script will save the updated CSV file with two new columns: one for the full hash and one for the truncated hash (if truncation length is provided).
- A log file will be generated if hash clashes are found when truncation is used.

## Notes

- The script will check for hash clashes only if truncation is used. Hash clashes are possible when hashes are truncated.

### Hash Algorithm Options

- blake2b
- blake2s
- md5
- sha1
- sha224
- sha256
- sha384
- sha512
- sha3_224
- sha3_256
- sha3_384
- sha3_512
- shake_128
- shake_256

To find all algorithms that are available, use `hashlib.algorithms_available` on your local Python environment.

```python
import hashlib

# Algorithms guaranteed to exist on all platforms
print("Algorithms guaranteed:", hashlib.algorithms_guaranteed)

# Algorithms that are available on the current platform
print("Algorithms available:", hashlib.algorithms_available)
```
