import re
from pathlib import Path


def extract_text_from_srt(filepath):
    """
    Removes timestamps and formatting from SRT subtitle files.
    
    Args:
        filepath (str): The path to a .txt or .srt file.
    
    Returns:
        None
    """
    valid_formats = ['.srt', '.txt', '.md']

    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Error: The file '{filepath}' was not found.")
    
    if not any(filepath.suffix == ext for ext in valid_formats):
        raise IOError(f"Error: Could not read the file contents of '{filepath.name}'. File format is invalid.")
    
    try:
        timestamp_pattern = r'\d+\s+\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\s*'
        tag_pattern = r'<.*?>'
        combined_pattern = rf"{timestamp_pattern}|{tag_pattern}"

        with open(filepath) as f:
            text = f.read()
            
        cleaned_text = re.sub(combined_pattern, "", text)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        
        return cleaned_text
        
    except RuntimeError:
        raise RuntimeError(f"Error: Could not read the file '{filepath}'")

def generate_word_list(text):
    pass