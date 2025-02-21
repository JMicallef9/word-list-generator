import re
from pathlib import Path
from collections import defaultdict
from string import punctuation
import csv


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
    """
    Generates a list of words and word frequencies in a given text.
    
    Args:
        text (str): Text containing the words to be counted.
    
    Returns:
        dict: A dictionary containing words and the number of times they appear in the text.
    """
    word_freq = defaultdict(int)
    punc_chars = punctuation + '¿¡'
    if text:
        words = text.lower().split()
        for word in words:
            word = re.sub(rf'[{punc_chars}]', '', word)
            word_freq[word] += 1 
    return word_freq

def convert_word_list_to_csv(words, filepath):
    sorted_words = sorted(words.items())

    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        for word, count in sorted_words:
            writer.writerow([f"{word}: {count}"])