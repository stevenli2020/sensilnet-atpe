import os
import re

# Configuration
DIRECTORIES_TO_SCAN = ["."]  # Scan everything from root
IGNORE_DIRS = {".git", ".venv", "__pycache__", ".gemini", ".idea", ".vscode"}
EXTENSIONS = {".md", ".txt"}

OUTPUT_FILENAME = "COMPRESSED_CONTEXT.md"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(PROJECT_ROOT, OUTPUT_FILENAME)

def is_structural_block(line):
    """Retain structural elements: Headers, Lists, Tables, Math, Code."""
    line = line.strip()
    if not line: return False
    if re.match(r'^(#+ |\||- |\* |\d+\. |Rule \d+|> )', line): return True
    if re.match(r'^(\$|```)', line): return True
    return False

def compress_file(file_path):
    if os.path.getsize(file_path) == 0:
        return ""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    compressed_lines = []
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            compressed_lines.append(line)
            continue
            
        if in_code_block or is_structural_block(line):
            compressed_lines.append(line)
            
    return "".join(compressed_lines)

def get_files_to_compress():
    files = []
    for directory in DIRECTORIES_TO_SCAN:
        search_path = os.path.join(PROJECT_ROOT, directory)
        for root, dirs, filenames in os.walk(search_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for filename in filenames:
                if any(filename.endswith(ext) for ext in EXTENSIONS):
                    file_path = os.path.join(root, filename)
                    # Don't re-compress the output file if it exists
                    if filename == OUTPUT_FILENAME:
                        continue
                    files.append(file_path)
    return sorted(files)

def run_compression():
    print(f"Generating {OUTPUT_FILENAME} in {PROJECT_ROOT}...")
    
    files_to_process = get_files_to_compress()
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
        outfile.write("# COMPRESSED PROJECT CONTEXT\n")
        outfile.write(f"Generated from all .md/.txt files in {DIRECTORIES_TO_SCAN}\n\n")
        
        for file_path in files_to_process:
            relative_path = os.path.relpath(file_path, PROJECT_ROOT)
            print(f"Ingesting: {relative_path}")
            outfile.write(f"\n\n## Source: {relative_path}\n")
            outfile.write(compress_file(file_path))
            
    print(f"Successfully generated: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    run_compression()
