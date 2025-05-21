import re
from pathlib import Path
from collections import defaultdict
from string import punctuation
import csv
from deep_translator import GoogleTranslator
import unicodedata
import docx
from pypdf import PdfReader
from bs4 import BeautifulSoup
import requests
from ebooklib import epub, ITEM_DOCUMENT


def extract_text_from_file(filepath):
    """
    Removes timestamps and formatting from SRT subtitle files.
    
    Args:
        filepath (str): The path to a file containing some text.
    
    Returns:
        str: The text from the given file, with timestamps and formatting removed.
    """
    valid_formats = ['.srt', '.txt', '.md', '.docx', '.pdf', '.epub']

    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Error: The file '{filepath}' was not found.")
    
    if not any(filepath.suffix == ext for ext in valid_formats):
        raise IOError(f"Error: Could not read the file contents of '{filepath.name}'. File format is invalid.")

    try:
        timestamp_pattern = r'\d+\s+\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\s*'
        tag_pattern = r'<.*?>'
        combined_pattern = rf"{timestamp_pattern}|{tag_pattern}"

        if filepath.suffix == '.docx':
            doc = docx.Document(filepath)
            text = '\n'.join([p.text for p in doc.paragraphs])

        elif filepath.suffix == '.pdf':
            pdf_reader = PdfReader(filepath)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        elif filepath.suffix == '.epub':
            book = epub.read_epub(str(filepath))
            text = ""
            for item in book.get_items():
                if item.get_type() == ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text += soup.get_text().strip()

        else:
            with open(filepath) as f:
                text = f.read()
            
        cleaned_text = re.sub(combined_pattern, "", text)
        cleaned_text = re.sub(r'[\u200B\u200C\u200D\u2060\uFEFF]', '', cleaned_text)
        cleaned_text = re.sub(r'\\an8}', '', cleaned_text)
        cleaned_text = unicodedata.normalize("NFC", cleaned_text)

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
    punc_chars = punctuation + '¿¡♪«»—©'
    if text:
        words = text.lower().split()
        for word in words:
            word = re.sub(rf'^[{punc_chars}]*|[{punc_chars}]*$', '', word)
            if word and not word.isnumeric():
                word_freq[word] += 1
    return word_freq

def check_for_new_words(text_words, anki_words):
    """
    Removes words from a word frequency dictionary if they are already stored in an existing set.
    
    Args:
        text_words (dict): A dictionary containing words and words frequencies.
        anki_words (set): A set containing unique words retrieved from an Anki deck.
    
    Returns:
        dict: A new dictionary with the words from the set removed.
    """
    new_words = {}
    for key, value in text_words.items():
        if key not in anki_words:
            new_words[key] = value
    return new_words

def convert_word_list_to_csv_with_translations(words, filepath, input_lang, target_lang):
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

    word_list = [word for word, count in sorted_words]
    translated_words = translator.translate_batch(word_list)

    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        for (word, count), translation in zip(sorted_words, translated_words):
            writer.writerow([f"{word}: {count}", translation])
    
def get_user_language(test_inputs=None):
    """
    Obtains user-specified language for translation purposes.

    Args:
        test_inputs (list): A list of test inputs representing languages (optional).
    
    Returns:
        str: A two-letter code representing the user-specified language.
    """
    valid_languages = GoogleTranslator().get_supported_languages(as_dict=True)

    if test_inputs:
        test_inputs = iter(test_inputs)

    while True:
        user_lang = next(test_inputs) if test_inputs else input("Please enter a language name or two-letter language code.\nTo see a list of all available languages, press L.\n")
        user_lang = user_lang.strip().lower()

        if user_lang in valid_languages.values():
            return user_lang
        elif user_lang in valid_languages.keys():
            return valid_languages[user_lang]
        elif user_lang == 'l':
            print('Available languages: ')
            for lang_name, lang_code in valid_languages.items():
                print(f'{lang_name}: {lang_code}')
            print('\n')
        else:
            print('Invalid input.')


def convert_word_list_to_csv(words, filepath):
    """
    Creates a CSV file containing words and word frequencies from a given text.

    Args:
        words (dict): A dictionary containing words and word frequencies.
        filepath (str): The intended filepath of the CSV file.
    
    Returns:
        None
    """
    sorted_words = sorted(words.items())

    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        for word, count in sorted_words:
            if word:
                writer.writerow([word, count])
    
def extract_file_list(dir, exts):
    """
    Extracts a list of files in a directory that match a list of extensions.

    Args:
        dir (str): A directory path.
        exts (list): A list of file extensions.
    
    Returns:
        list: A list of filepaths.
    """
    path = Path(dir)
    
    if not path.is_dir():
        raise ValueError(f"Invalid directory: {dir}")

    files = [file for file in path.glob("**/*") if file.suffix in exts]
    return files

def extract_text_from_url(url):
    """
    Extracts text from a URL, including body and header.

    Args:
        url (str): The URL of a webpage.

    Returns:
        str: The text content from the webpage.
    """
    try:
        response = requests.get(url, timeout=10)
        content = BeautifulSoup(response.content, "html.parser")

        for element in content(['script', 'style', 'noscript']):
            element.decompose()
        text = content.get_text(separator=' ', strip=True)
        return text

    except requests.RequestException:
        raise ValueError("Text extraction failed. URL may be invalid.")
