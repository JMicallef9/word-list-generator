from utils import extract_text_from_file, generate_word_list, check_for_new_words, convert_word_list_to_csv_with_translations, get_user_language
from anki_utils import get_anki_decks, get_words_from_deck
from pathlib import Path


def word_list_generator():
    while True:
        file_to_process = input("Enter the filepath of the file you want to process: ")
        if Path(file_to_process).is_file():
            break
        else:
            print("Invalid filepath. Please provide a valid filepath (e.g., /path/to/input.txt).")

    text = extract_text_from_file(file_to_process)

    anki_check = input("\nDo you want to filter the list using an Anki deck? (Y/n): ").strip().lower()

    if anki_check == 'y':
        pass

    else:

        while True:
            csv_name = input("\nPlease enter the destination filepath for the output CSV file: ")
            if not Path(csv_name).parent.exists():
                print("Invalid filepath. Please provide a valid filepath (e.g., /path/to/input.txt).")
                continue
            break


        print('\nWhat language is your text in?')
        text_lang = get_user_language()

        print('\nWhat language would you like translations in?')
        translation_lang = get_user_language()

        word_counts = generate_word_list(text)

        convert_word_list_to_csv_with_translations(word_counts, csv_name, text_lang, translation_lang)

        print(f"Word list file created: {csv_name}")

if __name__ == '__main__':
    word_list_generator()
