import os

# Define the project root based on this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "CONTEXT.md")

# Explicit list of files to ingest (No recursive wildcards)
FILES_TO_INGEST = [
    "WORKFLOWS.md",
    "HANDOFF.md",
    "docs/ARCHITECTURE.md",
    "docs/SPECIFICATIONS.md",
    "docs/RISK_REGISTER.md",
    "docs/KNOWN_LIMITATIONS.md",
    "docs/specs/pit_adjustment_engine_v1.md",
]

def generate_context():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        outfile.write("# Project Context Aggregation\n")
        outfile.write(f"Generated on: 2026-07-24\n\n")
        
        for file_path in FILES_TO_INGEST:
            full_path = os.path.join(PROJECT_ROOT, file_path)
            
            if not os.path.exists(full_path):
                print(f"Skipping missing file: {file_path}")
                continue
            
            print(f"Ingesting: {file_path}")
            outfile.write(f"\n\n---\n# Content from {file_path}\n---\n\n")
            
            with open(full_path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())

    print(f"\nSuccessfully generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_context()
