import os
import sys
import sqlite3
import argparse
from pathlib import Path
import re

try:
    import pyperclip
except ImportError:
    pyperclip = None

# GPT-4 Turbo context limit in characters
CONTEXT_LIMIT = 128000  # Approximate token to character conversion
PROJECT_DIR = Path(__file__).resolve().parent
STANDARD_IGNORE_FILE = PROJECT_DIR / 'standard.ctcignore'
GLOBAL_IGNORE_FILE = PROJECT_DIR / 'global.ctcignore'


def read_ignore_file(file_path):
    if file_path.is_file():
        with file_path.open('r') as file:
            return [line.strip() for line in file if line.strip()]
    return []


def read_ctcignore(directory):
    ignore_list = read_ignore_file(directory / '.ctcignore')
    global_ignore_list = read_ignore_file(GLOBAL_IGNORE_FILE)
    return ignore_list + global_ignore_list


def generate_ctcignore(directory):
    ignore_file_path = directory / '.ctcignore'
    if STANDARD_IGNORE_FILE.is_file():
        standard_ignore = STANDARD_IGNORE_FILE.read_text()
        ignore_file_path.write_text(standard_ignore)
        print(f"Standard .ctcignore file created at {ignore_file_path}")
    else:
        print(f"Standard ignore file not found at {STANDARD_IGNORE_FILE}")


def convert_db_to_text(file_path):
    output = []
    try:
        conn = sqlite3.connect(file_path)
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

        conn.close()
    except Exception as e:
        output.append(f"Could not read database {file_path}: {e}")

    return "\n".join(output)


def copy_content(content, output_to_file=False, output_file=None):
    tokens_used = len(content)

    if tokens_used > CONTEXT_LIMIT:
        print("Warning: The content exceeds the GPT-4 Turbo context window limit of 128k characters.")

    if output_to_file:
        output_file = output_file or 'clipboard.txt'
        output_path = Path.cwd() / output_file
        output_path.write_text(content, encoding='utf-8')
        print(f"Content has been written to {output_path}. Tokens used: {tokens_used}")
    else:
        if pyperclip and pyperclip.copy:
            try:
                pyperclip.copy(content)
                print(f"Content has been copied to the clipboard. Tokens used: {tokens_used}")
            except pyperclip.PyperclipException:
                print("Clipboard is not accessible. Consider using the '--output-to-file' option.")
        else:
            print("Pyperclip is not installed or clipboard is not accessible.")
            print("Install pyperclip or use the '--output-to-file' option.")


def copy_file_to_content(file_path):
    try:
        if file_path.suffix == '.db':
            content = convert_db_to_text(str(file_path))
        else:
            content = file_path.read_text(encoding='utf-8')
        return f"Filename: {file_path.name}\nContent:\n{content}\n"
    except Exception as e:
        print(f"Could not read file {file_path}: {e}")
        return ''


def should_ignore(file_path, ignore_patterns):
    for pattern in ignore_patterns:
        if pattern.startswith('*'):
            if file_path.name.endswith(pattern.lstrip('*')):
                return True
        elif pattern.endswith('*'):
            if file_path.name.startswith(pattern.rstrip('*')):
                return True
        elif pattern == file_path.name:
            return True
    return False


def copy_files_in_directory_to_content(directory, recursive=False):
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
            content = copy_file_to_content(file_path)
            if content:
                all_files_content.append(content)

    return "\n".join(all_files_content)


def main():
    parser = argparse.ArgumentParser(description='Copy file(s) content to clipboard or file.')
    parser.add_argument('path', nargs='?', default='.', help='File or directory path')
    parser.add_argument('--init-ignore', '-i', action='store_true', help='Initialize .ctcignore file')
    parser.add_argument('--recursive', '-r', action='store_true', help='Recursively include files in directories')
    parser.add_argument('--output', '-o', help='Output file path (used with --output-to-file)')
    parser.add_argument('--output-to-file', '-f', action='store_true', help='Write output to a file instead of the clipboard')

    args = parser.parse_args()
    path = Path(args.path).resolve()

    if args.init_ignore:
        generate_ctcignore(path)
    else:
        if path.is_file():
            content = copy_file_to_content(path)
            if content:
                copy_content(content, output_to_file=args.output_to_file, output_file=args.output)
        elif path.is_dir():
            content = copy_files_in_directory_to_content(path, args.recursive)
            if content:
                copy_content(content, output_to_file=args.output_to_file, output_file=args.output)
        else:
            print(f"The specified path {path} is neither a file nor a directory.")


if __name__ == "__main__":
    main()
