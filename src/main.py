from utils import extract_text_from_file, generate_word_list, check_for_new_words, convert_word_list_to_csv, get_user_language
from anki_utils import get_anki_decks, get_words_from_deck
from deep_translator import GoogleTranslator


def word_list_generator():
    file_to_process = input("Please enter the filepath to be processed: ")

    text = extract_text_from_file(file_to_process)

    anki_check = input("Do you want to filter the list using an Anki deck? (Y/n): ").strip().lower()

    if anki_check == 'y':
        pass

    else:
        csv_name = input("Please enter a filename/directory for the CSV file: ")

        text_lang = get_user_language('What language is your text in?')

        translation_lang = get_user_language('What language would you like translations in?')

        convert_word_list_to_csv(text, csv_name, text_lang, translation_lang)

        print(f"Word list file created: {csv_name}")



