from utils import extract_text_from_file, generate_word_list, check_for_new_words, get_user_language, convert_word_list_to_csv
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

    print(f"\nText successfully extracted from the following file: {file_to_process}")

    word_counts = generate_word_list(text)

    anki_check = input("\nDo you want to filter the word list using an Anki deck? (Y/n): ").strip().lower()

    if anki_check == 'y':
        decks = get_anki_decks()

        print("\nWhich deck(s) would you like to filter by? Please select one or more options, separated by commas.\n")

        for i, deck in enumerate(decks, 1):
            print(f"{i}: {deck}")
        
        user_choice = input("Enter your choice(s): ")

        selected_options = [int(num.strip()) for num in user_choice.split(",")]

        selected_decks = [decks[num - 1] for num in selected_options]

        print("You selected the following decks:\n")

        for deck in selected_decks:
            print(f"{deck}\n")
            deck_words = get_words_from_deck(deck)
            word_counts = check_for_new_words(word_counts, deck_words)

    while True:
        csv_name = input("\nPlease enter the destination filepath for the output CSV file: ")

        path_obj = Path(csv_name)

        if path_obj.suffix.lower() != ".csv":
            path_obj = path_obj.with_suffix(".csv")

        if not path_obj.parent.exists():
            print("Invalid filepath. Please provide a valid filepath (e.g., /path/to/input.txt).")
            continue
        break

    print('\nCreating CSV file...')

    convert_word_list_to_csv(word_counts, path_obj)

    print(f"Word list file created: {path_obj}")


if __name__ == '__main__':
    word_list_generator()