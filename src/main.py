from utils import extract_text_from_file, generate_word_list, check_for_new_words, convert_word_list_to_csv
from anki_utils import get_anki_decks, get_words_from_deck

def word_list_generator():
    file_to_process = input("Please enter the filepath to be processed.")

    text = extract_text_from_file(file_to_process)

    

