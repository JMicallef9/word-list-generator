from utils import extract_text_from_file, generate_word_list, check_for_new_words, get_user_language, convert_word_list_to_csv
from anki_utils import get_anki_decks, get_words_from_deck
from pathlib import Path
import time


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

    while True:
        if anki_check == 'y':
            decks = get_anki_decks()

            print("\nWhich deck(s) would you like to filter by? Please select one or more options, separated by commas.\n")

            for i, deck in enumerate(decks, 1):
                print(f"{i}: {deck}")
            
            user_choice = input("Enter your choice(s) or press C to cancel: ").strip().lower()

            if user_choice == 'c':
                print("\nDeck selection cancelled. Proceeding without Anki filtering.")
                break
            
            try:
                selected_options = [int(num.strip()) for num in user_choice.split(",")]

                if not all(1 <= num <= len(decks) for num in selected_options):
                    print(f"\nInvalid input. Please enter a number between 1 and {len(decks)}.")
                    time.sleep(0.5)
                    continue

                selected_decks = [decks[num - 1] for num in selected_options]

                print("You selected the following decks:\n")

                for deck in selected_decks:
                    print(f"{deck}\n")
                    deck_words = get_words_from_deck(deck)
                    word_counts = check_for_new_words(word_counts, deck_words)
                
                break

            except ValueError:
                print("\nInvalid input. Please enter one or more numbers separated by commas.")
                time.sleep(0.5)
                continue
        else:
            break

    while True:
        csv_name = input("\nPlease enter the destination filepath for the output CSV file: ")

        csv_path_obj = Path(csv_name)

        if csv_path_obj.suffix.lower() != ".csv":
            csv_path_obj = csv_path_obj.with_suffix(".csv")

        if not csv_path_obj.parent.exists():
            print("Invalid filepath. Please provide a valid filepath (e.g., /path/to/input.txt).")
            continue
        break

    print('\nCreating CSV file...')

    convert_word_list_to_csv(word_counts, csv_path_obj)

    print(f"Word list file created: {csv_path_obj}")


if __name__ == '__main__':
    word_list_generator()