import re
from pathlib import Path
from collections import defaultdict
from string import punctuation
import csv
from deep_translator import GoogleTranslator



def extract_text_from_file(filepath):
    """
    Removes timestamps and formatting from SRT subtitle files.
    
    Args:
        filepath (str): The path to a .txt or .srt file.
    
    Returns:
        str: The text from the given file, with timestamps and formatting removed.
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

def check_for_new_words(text_words, anki_words):
    """
    Removes words from a word frequency dictionary if they are already stored in an existing set.
    
    Args:
        text_words (dict): A dictionary containing words and words frequencies.
        anki_words (set): A set containing unique words retrieved from an Anki deck.
    
    Returns:
        A new dictionary with the words from the set removed.
    """
    new_words = {}
    for key, value in text_words.items():
        if key not in anki_words:
            new_words[key] = value
    return new_words

def convert_word_list_to_csv(words, filepath, input_lang, target_lang):
    """
    Creates a CSV file containing words and their translations.

    Args:
        words (dict): A dictionary containing words and word frequencies.
        filepath (str): The intended filepath of the CSV file.
        input_lang (str): The language code representing the language of the inputted words.
        target_lang (str): The language code of the language in which translations will be provided in the CSV file.
    
    Returns:
        None
    """
    sorted_words = sorted(words.items())
    translator = GoogleTranslator(source=input_lang, target=target_lang)

    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        for word, count in sorted_words:
            writer.writerow([f"{word}: {count}", translator.translate(word)])