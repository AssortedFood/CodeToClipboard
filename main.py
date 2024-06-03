import os
import pyperclip
import sys
import sqlite3

# GPT-4 Turbo context limit in characters
CONTEXT_LIMIT = 128000  # Approximate token to character conversion
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STANDARD_IGNORE_FILE = os.path.join(PROJECT_DIR, 'standard.ctcignore')
GLOBAL_IGNORE_FILE = os.path.join(PROJECT_DIR, 'global.ctcignore')

def read_ignore_file(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    return []

def read_ctcignore(directory):
    ignore_list = read_ignore_file(os.path.join(directory, '.ctcignore'))
    global_ignore_list = read_ignore_file(GLOBAL_IGNORE_FILE)
    return ignore_list + global_ignore_list

def generate_ctcignore(directory):
    ignore_file_path = os.path.join(directory, '.ctcignore')
    if os.path.isfile(STANDARD_IGNORE_FILE):
        with open(STANDARD_IGNORE_FILE, 'r') as file:
            standard_ignore = file.readlines()
        with open(ignore_file_path, 'w') as file:
            file.writelines(standard_ignore)
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

            # Get table contents
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            output.append("Contents:")
            for row in rows:
                output.append(f"  {row}")
            output.append("\n")
            
        conn.close()
    except Exception as e:
        output.append(f"Could not read database {file_path}: {e}")
    
    return "\n".join(output)

def copy_file_to_clipboard(file_path):
    try:
        if file_path.endswith('.db'):
            content = convert_db_to_text(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        clipboard_content = f"Filename: {os.path.basename(file_path)}\nContent:\n{content}\n"
    except Exception as e:
        print(f"Could not read file {file_path}: {e}")
        return
    
    tokens_used = len(clipboard_content)
    
    if tokens_used > CONTEXT_LIMIT:
        print("Warning: The clipboard content exceeds the GPT-4 Turbo context window limit of 128k characters.")
    
    pyperclip.copy(clipboard_content)
    print(f"File content has been copied to the clipboard. Tokens used: {tokens_used}")

def copy_files_in_directory_to_clipboard(directory):
    ignore_list = read_ctcignore(directory)
    all_files_content = []
    
    for filename in os.listdir(directory):
        if any([filename == pattern.strip() or filename.endswith(pattern.strip().lstrip('*')) for pattern in ignore_list]):
            continue

        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            try:
                if filename.endswith('.db'):
                    content = convert_db_to_text(file_path)
                else:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                all_files_content.append(f"Filename: {filename}\nContent:\n{content}\n")
            except Exception as e:
                print(f"Could not read file {filename}: {e}")
    
    clipboard_content = "\n".join(all_files_content)
    tokens_used = len(clipboard_content)
    
    if tokens_used > CONTEXT_LIMIT:
        print("Warning: The clipboard content exceeds the GPT-4 Turbo context window limit of 128k characters.")
    
    pyperclip.copy(clipboard_content)
    print(f"All file names and contents have been copied to the clipboard. Tokens used: {tokens_used}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--init-ignore', '--i']:
            directory = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
            generate_ctcignore(directory)
        else:
            path = sys.argv[1]
            if os.path.isdir(path):
                copy_files_in_directory_to_clipboard(path)
            elif os.path.isfile(path):
                copy_file_to_clipboard(path)
            else:
                print(f"The specified path {path} is neither a file nor a directory.")
    else:
        directory = os.getcwd()
        copy_files_in_directory_to_clipboard(directory)
