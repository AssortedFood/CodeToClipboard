import sys
import sqlite3
import argparse
from pathlib import Path
import fnmatch
import logging

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    import tiktoken
except ImportError:
    tiktoken = None

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Read configuration from config.ini if available
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# GPT-4 Turbo context limit in tokens
CONTEXT_LIMIT = int(config.get('DEFAULT', 'context_limit', fallback='128000'))

PROJECT_DIR = Path(__file__).resolve().parent
STANDARD_IGNORE_FILE = PROJECT_DIR / config.get('DEFAULT', 'standard_ignore_file', fallback='standard.ctcignore')
GLOBAL_IGNORE_FILE = PROJECT_DIR / config.get('DEFAULT', 'global_ignore_file', fallback='global.ctcignore')


def estimate_tokens(text, model_name='gpt-4'):
    """
    Estimates the number of tokens in the text using tiktoken.

    Args:
        text (str): The text to estimate tokens for.
        model_name (str): The model name to use for encoding.

    Returns:
        int: The estimated number of tokens.
    """
    if tiktoken:
        encoding = tiktoken.encoding_for_model(model_name)
        tokens = encoding.encode(text)
        return len(tokens)
    else:
        # Fallback to character count if tiktoken is not installed
        return len(text)


def read_ignore_file(file_path):
    """
    Reads ignore patterns from a file.

    Args:
        file_path (Path): The path to the ignore file.

    Returns:
        list: A list of ignore patterns.
    """
    if file_path.is_file():
        try:
            with file_path.open('r', encoding='utf-8') as file:
                return [line.strip() for line in file if line.strip()]
        except Exception as e:
            logging.error(f"Could not read ignore file {file_path}: {e}")
    return []


def read_ctcignore(directory):
    """
    Reads ignore patterns from .ctcignore and global ignore files.

    Args:
        directory (Path): The directory to look for the .ctcignore file.

    Returns:
        list: A combined list of ignore patterns.
    """
    ignore_list = read_ignore_file(directory / '.ctcignore')
    global_ignore_list = read_ignore_file(GLOBAL_IGNORE_FILE)
    return ignore_list + global_ignore_list


def generate_ctcignore(directory):
    """
    Generates a standard .ctcignore file in the specified directory.

    Args:
        directory (Path): The directory to create the .ctcignore file in.
    """
    ignore_file_path = directory / '.ctcignore'
    if STANDARD_IGNORE_FILE.is_file():
        try:
            standard_ignore = STANDARD_IGNORE_FILE.read_text(encoding='utf-8')
            ignore_file_path.write_text(standard_ignore, encoding='utf-8')
            logging.info(f"Standard .ctcignore file created at {ignore_file_path}")
        except Exception as e:
            logging.error(f"Could not write .ctcignore file: {e}")
    else:
        logging.error(f"Standard ignore file not found at {STANDARD_IGNORE_FILE}")


def convert_db_to_text(file_path):
    """
    Converts a SQLite database schema and row counts to text.

    Args:
        file_path (str): The path to the database file.

    Returns:
        str: The textual representation of the database schema and row counts.
    """
    output = []
    try:
        with sqlite3.connect(file_path) as conn:
            cursor = conn.cursor()

            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                output.append(f"Table: {table_name}")

                # Get table schema
                cursor.execute(f"PRAGMA table_info({table_name});")
                schema = cursor.fetchall()
                output.append("Schema:")
                for column in schema:
                    output.append(f"  {column[1]} ({column[2]})")

                # Get number of rows
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                row_count = cursor.fetchone()[0]
                output.append(f"Number of rows: {row_count}")

                output.append("\n")

    except sqlite3.DatabaseError as e:
        output.append(f"Could not read database {file_path}: {e}")
    except Exception as e:
        output.append(f"An unexpected error occurred: {e}")

    return "\n".join(output)


def copy_content(content, output_to_file=False, output_file=None):
    """
    Copies content to the clipboard or writes it to a file.

    Args:
        content (str): The content to copy or write.
        output_to_file (bool): Whether to write the content to a file.
        output_file (str): The output file path if writing to a file.
    """
    tokens_used = estimate_tokens(content)

    if tokens_used > CONTEXT_LIMIT:
        logging.warning(f"The content exceeds the GPT-4 Turbo context window limit of {CONTEXT_LIMIT} tokens.")

    if output_to_file:
        output_file = output_file or 'clipboard.txt'
        output_path = Path.cwd() / output_file
        try:
            output_path.write_text(content, encoding='utf-8')
            logging.info(f"Content has been written to {output_path}. Tokens used: {tokens_used}")
        except Exception as e:
            logging.error(f"Could not write to file {output_path}: {e}")
    else:
        if pyperclip and pyperclip.copy:
            try:
                pyperclip.copy(content)
                logging.info(f"Content has been copied to the clipboard. Tokens used: {tokens_used}")
            except pyperclip.PyperclipException:
                logging.error("Clipboard is not accessible. Consider using the '--output-to-file' option.")
        else:
            logging.error("Pyperclip is not installed or clipboard is not accessible.")
            logging.error("Install pyperclip or use the '--output-to-file' option.")


def copy_file_to_content(file_path, encoding):
    """
    Reads the content of a file and formats it for output.

    Args:
        file_path (Path): The path to the file.
        encoding (str): The encoding to use when reading the file.

    Returns:
        str: The formatted content of the file.
    """
    try:
        if file_path.suffix == '.db':
            content = convert_db_to_text(str(file_path))
        else:
            content = file_path.read_text(encoding=encoding, errors='replace')
        return f"Filename: {file_path.name}\nContent:\n{content}\n"
    except Exception as e:
        logging.error(f"Could not read file {file_path}: {e}")
        return ''


def should_ignore(file_path, ignore_patterns):
    """
    Determines whether a file should be ignored based on ignore patterns.

    Args:
        file_path (Path): The path to the file relative to the root directory.
        ignore_patterns (list): A list of ignore patterns.

    Returns:
        bool: True if the file should be ignored, False otherwise.
    """
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(file_path.name, pattern):
            return True
    return False


def copy_files_in_directory_to_content(directory, recursive=False, encoding='utf-8'):
    """
    Collects content from files in a directory, optionally recursively.

    Args:
        directory (Path): The directory to search for files.
        recursive (bool): Whether to search directories recursively.
        encoding (str): The encoding to use when reading files.

    Returns:
        str: The combined content from all files.
    """
    ignore_patterns = read_ctcignore(directory)
    all_files_content = []

    if recursive:
        files = directory.rglob('*')
    else:
        files = directory.iterdir()

    for file_path in files:
        if file_path.is_file():
            relative_path = file_path.relative_to(directory)
            if should_ignore(relative_path, ignore_patterns):
                continue
            content = copy_file_to_content(file_path, encoding)
            if content:
                all_files_content.append(content)

    return "\n".join(all_files_content)


def main():
    """
    Main function to parse arguments and execute the script logic.
    """
    parser = argparse.ArgumentParser(
        description='Copy file(s) content to clipboard or file.',
        epilog='Examples:\n'
               '  python script.py /path/to/file.txt\n'
               '  python script.py /path/to/directory --recursive\n'
               '  python script.py --init-ignore\n',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('path', nargs='?', default='.', help='File or directory path')
    parser.add_argument('--init-ignore', '-i', action='store_true', help='Initialize .ctcignore file')
    parser.add_argument('--recursive', '-r', action='store_true', help='Recursively include files in directories')
    parser.add_argument('--output', '-o', metavar='FILE', help='Output file path (used with --output-to-file)')
    parser.add_argument('--output-to-file', '-f', action='store_true', help='Write output to a file instead of the clipboard')
    parser.add_argument('--encoding', '-e', default='utf-8', help='Specify file encoding')

    args = parser.parse_args()
    path = Path(args.path).resolve()

    if args.init_ignore:
        generate_ctcignore(path)
        return

    if not path.exists():
        logging.error(f"The specified path {path} does not exist.")
        sys.exit(1)

    if path.is_file():
        content = copy_file_to_content(path, args.encoding)
        if content:
            copy_content(content, output_to_file=args.output_to_file, output_file=args.output)
    elif path.is_dir():
        content = copy_files_in_directory_to_content(path, args.recursive, args.encoding)
        if content:
            copy_content(content, output_to_file=args.output_to_file, output_file=args.output)
    else:
        logging.error(f"The specified path {path} is neither a file nor a directory.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")
        sys.exit(0)
