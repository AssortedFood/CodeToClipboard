
# CodeToClipboard

CodeToClipboard is a Python tool designed to assist developers by copying the names and contents of all files in a specified directory to the clipboard. This is particularly useful for dumping high volumes of data from multiple files into ChatGPT when working on large projects.

## Features

- Copies the name and content of every file in a directory to the clipboard.
- Handles multiple text files efficiently.
- Easy integration with ChatGPT for quick data dumps.

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

1. Open the `main.py` script.

2. Specify the directory containing your files by replacing the placeholder path:

    ```python
    # Specify your directory here
    directory = "/path/to/your/directory"
    ```

3. Run the script:

    ```sh
    python main.py
    ```

4. The names and contents of all files in the specified directory will be copied to your clipboard, ready to be pasted wherever needed.

### Terminal Usage

To use `CodeToClipboard` from the terminal, you can call the script with a directory as an argument:

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
    function ctc { python "C:\path\to\your\script\main.py" $args }
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
    alias ctc='python /path/to/your/script/main.py'
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

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for more details.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## Contact

For any questions or suggestions, please open an issue on GitHub.
