import os
import sys
import pyperclip
import re

SENSITIVE_KEYS = ["key", "clientsecret", "password", "pwd", "issuer", "audience","domain","clientid","tenantdd","tenantid"]

def mask_sensitive_values(content):
    pattern = r'"(' + '|'.join(SENSITIVE_KEYS) + r')":\s*"([^"]*)"'
    return re.sub(pattern, lambda m: f'"{m.group(1)}": "xxxxxxx"', content, flags=re.IGNORECASE)

def read_code_files(directory):
    code_extensions = [".py", ".cs", ".json", ".http", ".yml", ".csproj"]
    excluded_dirs = {'bin', 'obj'}
    file_contents = []

    print(f"Processing directory: {directory}")

    try:
        for root, dirs, files in os.walk(directory):
            # Exclude specified directories
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in code_extensions):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding='utf-8', errors='replace') as code_file:
                        content = code_file.read()
                        masked_content = mask_sensitive_values(content)
                        file_contents.append(f"File: {file_path}\nContent:\n{masked_content}\n---\n")
                        print(f"Processed file: {file_path}")

        if file_contents:
            combined_content = "\n".join(file_contents)
            pyperclip.copy(combined_content)
            print("Code file contents copied to the clipboard.")
        else:
            print("No code files found in the specified directory and its subdirectories.")
    except Exception as e:
        import logging
        logging.basicConfig(filename='copy_code_files_2.log', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.exception(f"An error occurred: {str(e)}")
        print("An error occurred. Please check the log file for details.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        print("Example: python script.py /path/to/directory")
    else:
        directory = sys.argv[1]
        read_code_files(directory)