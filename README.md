# CodeToClipboard

CodeToClipboard is a Python tool designed to assist developers by copying the names and contents of files in a specified directory to the clipboard or to a file. This is particularly useful for dumping high volumes of data from multiple files into ChatGPT when working on large projects.

## Features

- Copies the name and content of files in a directory to the clipboard or to a file.
- Handles multiple text files efficiently.
- Converts `.db` files by extracting table schemas and row counts.
- Supports recursive directory traversal with an optional flag.
- Allows specifying files to ignore using `.ctcignore` files.
- Configurable via command-line arguments and optional `config.ini` file.
- Provides detailed logging output for better debugging and user feedback.

## Requirements

- **Python 3.6 or higher**
- `pyperclip` library (for clipboard functionality)
- `tiktoken` library (optional, for accurate token estimation)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/CodeToClipboard.git
    ```

2. **Navigate to the project directory:**

    ```sh
    cd CodeToClipboard
    ```

3. **Install the required libraries:**

    ```sh
    pip install -r requirements.txt
    ```

    The `requirements.txt` file includes:

    ```
    pyperclip
    tiktoken
    ```

    *Note:* If you don't need token estimation, you can skip installing `tiktoken`.

## Usage

The script can copy file contents to the clipboard or write them to a file, with several configurable options.

### Command-Line Arguments

- `path`: (Optional) File or directory path. Defaults to the current working directory if not specified.
- `--init-ignore`, `-i`: Initialize a standard `.ctcignore` file in the specified directory.
- `--recursive`, `-r`: Recursively include files in directories.
- `--output-to-file`, `-f`: Write output to a file instead of the clipboard.
- `--output`, `-o`: Specify the output file path (used with `--output-to-file`).
- `--encoding`, `-e`: Specify the file encoding (default is `utf-8`).

### Generating a Standard `.ctcignore` File

To create a `.ctcignore` file with standard ignore patterns:

```sh
python main.py --init-ignore /path/to/your/directory
```

Or use the shorthand:

```sh
python main.py -i /path/to/your/directory
```

If no directory is specified, the `.ctcignore` file will be created in the current working directory:

```sh
python main.py --init-ignore
```

### Copying Files to Clipboard

**Copy all files in the current directory to the clipboard:**

```sh
python main.py
```

**Copy all files in a specified directory to the clipboard:**

```sh
python main.py /path/to/your/directory
```

**Recursively copy all files in a directory to the clipboard:**

```sh
python main.py /path/to/your/directory --recursive
```

**Specify file encoding if needed:**

```sh
python main.py /path/to/your/directory --encoding utf-8
```

### Writing Output to a File

If you prefer to write the output to a file instead of copying it to the clipboard, use the `--output-to-file` or `-f` flag.

**Write output to `clipboard.txt` in the current directory:**

```sh
python main.py /path/to/your/directory --output-to-file
```

**Specify a custom output file name:**

```sh
python main.py /path/to/your/directory --output-to-file --output output.txt
```

### Examples

**Copy a single file to the clipboard:**

```sh
python main.py /path/to/file.txt
```

**Copy files recursively and write to a file:**

```sh
python main.py /path/to/directory --recursive --output-to-file --output all_files.txt
```

### Adding as an Alias

#### PowerShell

1. **Open PowerShell**: Start by opening PowerShell.

2. **Create Profile File if It Doesn't Exist**:

    ```powershell
    if (!(Test-Path -Path $PROFILE)) {
        New-Item -Type File -Path $PROFILE -Force
    }
    ```

3. **Edit Profile File**: Open the profile file in a text editor:

    ```powershell
    notepad $PROFILE
    ```

4. **Add Alias to Profile**: Add the following function to the profile file:

    ```powershell
    function ctc { python "C:\Users\YourUsername\Projects\CodeToClipboard\main.py" $args }
    ```

    Replace `C:\Users\YourUsername\Projects\CodeToClipboard\main.py` with the actual path to `main.py`.

    **Usage:**

    ```sh
    ctc /path/to/your/directory
    ```

5. **Save and Close**: Save the changes and close the text editor.

6. **Reload Profile**: Reload the PowerShell profile:

    ```powershell
    . $PROFILE
    ```

#### Bash

1. **Open Terminal**: Start by opening your terminal.

2. **Edit Bash Profile**:

    ```bash
    nano ~/.bashrc
    ```

3. **Add Alias to Bash Profile**: Add the following alias to the `.bashrc` file:

    ```bash
    alias ctc='python /path/to/CodeToClipboard/main.py'
    ```

    Replace `/path/to/CodeToClipboard/main.py` with the actual path to `main.py`.

    **Usage:**

    ```sh
    ctc /path/to/your/directory
    ```

    Or, you can `cd` to the directory and simply run:

    ```sh
    ctc
    ```

4. **Save and Close**: Save the changes and close the editor (in `nano`, press `Ctrl+O` to write out and `Ctrl+X` to exit).

5. **Reload Bash Profile**: Reload the profile to apply the changes:

    ```bash
    source ~/.bashrc
    ```

## Configuration File

You can create a `config.ini` file in the same directory as `main.py` to override default settings. Here's an example:

```ini
[DEFAULT]
context_limit = 128000
standard_ignore_file = standard.ctcignore
global_ignore_file = global.ctcignore
```

- `context_limit`: Sets the maximum number of tokens.
- `standard_ignore_file`: Specifies the path to the standard ignore file.
- `global_ignore_file`: Specifies the path to the global ignore file.

## Example

Given a directory with the following structure:

```
/path/to/your/directory
├── file1.txt
├── file2.txt
└── data.db
```

Running the script:

```sh
python main.py /path/to/your/directory --recursive --output-to-file --output output.txt
```

Will create `output.txt` with contents similar to:

```
Filename: file1.txt
Content:
<content of file1.txt>

Filename: file2.txt
Content:
<content of file2.txt>

Filename: data.db
Content:
Table: users
Schema:
  id (INTEGER)
  name (TEXT)
  email (TEXT)
Number of rows: 150

Table: orders
Schema:
  order_id (INTEGER)
  user_id (INTEGER)
  amount (REAL)
Number of rows: 320
```

## Logging

The script provides detailed logging output to the terminal, including informational messages, warnings, and errors. This helps in tracking the script's progress and diagnosing any issues.

## Handling Large Content

If the combined content exceeds the predicted context window limit, a warning will be displayed:

```
WARNING: The content exceeds the predicted Turbo context window limit of 128000 tokens.
```

You may need to adjust the content or process files in smaller batches.

## Error Handling

The script includes robust error handling to manage issues such as file read errors, encoding problems, and database access errors. Informative messages are logged to assist in troubleshooting.

## Requirements File

The `requirements.txt` file lists the necessary Python packages without version numbers:

```
pyperclip
tiktoken
```

Install the dependencies using:

```sh
pip install -r requirements.txt
```

## License

This project is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for more details.

## Contributing

1. **Fork the repository.**
2. **Create a new branch:**

    ```sh
    git checkout -b feature-branch
    ```

3. **Make your changes.**
4. **Commit your changes:**

    ```sh
    git commit -am 'Add some feature'
    ```

5. **Push to the branch:**

    ```sh
    git push origin feature-branch
    ```

6. **Create a new Pull Request.**

## Contact

For any questions or suggestions, please open an issue on GitHub.
