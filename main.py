import os
import pyperclip
import sys

# GPT-4 Turbo context limit in characters
CONTEXT_LIMIT = 128000  # Approximate token to character conversion
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STANDARD_IGNORE_FILE = os.path.join(PROJECT_DIR, 'standard.ctcignore')

def read_ctcignore(directory):
    ignore_file_path = os.path.join(directory, '.ctcignore')
    if os.path.isfile(ignore_file_path):
        with open(ignore_file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    return []

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

def copy_files_to_clipboard(directory):
    ignore_list = read_ctcignore(directory)
    all_files_content = []
    
    for filename in os.listdir(directory):
        if any([filename == pattern.strip() or filename.endswith(pattern.strip().lstrip('*')) for pattern in ignore_list]):
            continue

        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    all_files_content.append(f"Filename: {filename}\nContent:\n{content}\n")
            except Exception as e:
                print(f"Could not read file {filename}: {e}")
    
    clipboard_content = "\n".join(all_files_content)
    
    if len(clipboard_content) > CONTEXT_LIMIT:
        print("Warning: The clipboard content exceeds the GPT-4 Turbo context window limit of 128k characters.")
    
    pyperclip.copy(clipboard_content)
    print("All file names and contents have been copied to the clipboard.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--init-ignore', '--i']:
            directory = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
            generate_ctcignore(directory)
        else:
            directory = sys.argv[1]
            copy_files_to_clipboard(directory)
    else:
        directory = os.getcwd()
        copy_files_to_clipboard(directory)
