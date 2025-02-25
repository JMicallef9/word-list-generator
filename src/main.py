from utils import extract_text_from_file, generate_word_list, check_for_new_words, convert_word_list_to_csv, get_user_language
from anki_utils import get_anki_decks, get_words_from_deck


def word_list_generator():
    file_to_process = input("Please enter the filepath to be processed: ")
    # FileNotFoundError

    text = extract_text_from_file(file_to_process)

    anki_check = input("Do you want to filter the list using an Anki deck? (Y/n): ").strip().lower()

    if anki_check == 'y':
        pass

    else:
        csv_name = input("Please enter a filename/directory for the CSV file: ")

        print('What language is your text in?')
        text_lang = get_user_language()

        print('What language would you like translations in?')
        translation_lang = get_user_language()

        word_counts = generate_word_list(text)

        convert_word_list_to_csv(word_counts, csv_name, text_lang, translation_lang)

        print(f"Word list file created: {csv_name}")

if __name__ == '__main__':
    word_list_generator()
