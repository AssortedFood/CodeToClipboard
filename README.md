
# CodeToClipboard

CodeToClipboard is a Python tool designed to assist developers by copying the names and contents of all files in a specified directory to the clipboard. This is particularly useful for dumping high volumes of data from multiple files into ChatGPT when working on large projects.

## Features

- Copies the name and content of every file in a directory to the clipboard.
- Handles multiple text files efficiently.
- Easy integration with ChatGPT for quick data dumps.
- Can generate a standard `.ctcignore` file to specify files to ignore.

## Requirements

- Python 3.x
- `pyperclip` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/CodeToClipboard.git
    ```

2. Navigate to the project directory:

    ```sh
    cd CodeToClipboard
    ```

3. Install the required libraries:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Generate a Standard `.ctcignore` File**:
    ```sh
    python main.py --init-ignore /path/to/your/directory
    ```
    Or use the shorthand:
    ```sh
    python main.py --i /path/to/your/directory
    ```
    If no directory is specified, the `.ctcignore` file will be created in the current working directory:
    ```sh
    python main.py --init-ignore
    ```

2. **Run the Script to Copy Files**:
    - Without Arguments: Uses the current working directory.
        ```sh
        python main.py
        ```
    - With Directory Argument: Specify a directory as an argument.
        ```sh
        python main.py /path/to/your/directory
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

4. **Add Alias to Profile**: Add the following line to the profile file:
    ```powershell
    function ctc { python "C:\Users\Hamoon\Projects\CodeToClipboard\main.py" $args }
    ```
    Usage:
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

3. **Add Alias to Bash Profile**: Add the following line to the `.bashrc` file:
    ```bash
    alias ctc='python /mnt/c/Users/Hamoon/Projects/CodeToClipboard/main.py'
    ```
### Usage

```sh
ctc /path/to/your/directory
```
Or, you can `cd` to the directory and simply run:
```sh
ctc
```
To generate a `.ctcignore` file:
```sh
ctc --init-ignore /path/to/your/directory
```
Or use the shorthand:
```sh
ctc -i /path/to/your/directory
```

4. **Save and Close**: Save the changes and close the editor (in `nano`, you do this with `Ctrl+O` to write out and `Ctrl+X` to exit).

5. **Reload Bash Profile**: Reload the profile to apply the changes:
    ```bash
    source ~/.bashrc
    ```

### Example

Given a directory with the following structure:

```
/path/to/your/directory
├── file1.txt
├── file2.txt
└── file3.txt
```

The script will copy the following content to the clipboard:

```
Filename: file1.txt
Content:
<content of file1.txt>

Filename: file2.txt
Content:
<content of file2.txt>

Filename: file3.txt
Content:
<content of file3.txt>
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## Contact

For any questions or suggestions, please open an issue on GitHub.
