"""
The purpose of the script is to:
    - Extract words from a file.
    - Filter the words using an Anki deck (optional).
    - Export a word list to a .csv file.

Usage:
    Run the script and follow the prompts to:
    - Provide a file (.txt, .srt, .md, .docx, .pdf, .epub, .mkv) or a URL.
    - Optionally filter words using an Anki deck
    - Export the processed word list to a CSV file

Dependencies:
    - utils.py (contains text extraction and word list generation functions)
    - anki_utils.py (handles interaction with Anki)
    - pathlib (for file path handling)

Example:
    $ python script.py
"""


from utils import (
    extract_text_from_file,
    generate_word_list,
    check_for_new_words,
    convert_word_list_to_csv,
    extract_file_list,
    extract_text_from_url,
    list_subtitle_tracks,
    extract_text_from_mkv)
from anki_utils import get_anki_decks, get_words_from_deck
from pathlib import Path
import time
import sys
from urllib.parse import urlparse


def word_list_generator():
    """Runs the interactive word list generation process."""
    file_texts = []
    valid_extensions = [
        '.srt', '.txt', '.md', '.docx', '.pdf', '.epub', '.mkv'
        ]

    while True:
        path_input = input(
            "Enter a new file, directory path or URL "
            "that you wish to process, or press A to continue: "
            ).strip().strip('"').strip("'")

        if path_input.lower() == 'a':
            break

        parsed = urlparse(path_input)
        is_url = parsed.scheme in ("http", "https") and parsed.netloc != ""

        if is_url:
            try:
                text = extract_text_from_url(path_input)
                file_texts.append(text)
                print(
                    "\nText processed successfully. "
                    "To add more text to the word list, "
                    "enter another URL or filepath."
                    )
                default_name = Path(parsed.path).stem + ".csv"
                default_dir = Path.cwd()
                continue
            except ValueError:
                print("\nError. Invalid URL provided.")
                time.sleep(0.5)
                continue

        else:
            path = Path(path_input)
            default_name = path.stem + ".csv"
            default_dir = path.parent

            if path.is_dir():
                files = extract_file_list(path_input, valid_extensions)
                if not files:
                    print(
                        "\nNo valid files found "
                        "in directory. Please try again."
                        )
                    continue
                print(
                    f"\nProcessing {len(files)} files from "
                    f"the following directory: {path_input}"
                    )
                for file in files:
                    try:
                        text = extract_text_from_file(file)
                        file_texts.append(text)
                        print(f"Processed file: {file}")
                    except Exception as e:
                        print(f"Error processing {file}: {e}")

            elif path.is_file():

                if path.suffix == '.mkv':
                    tracks = list_subtitle_tracks(path_input)

                    if not tracks:
                        print(
                            "No valid subtitle tracks found. "
                            "Please try another file."
                            )
                        continue

                    print("\nAvailable subtitle tracks:\n")

                    for track in tracks:
                        print(f"{track['id']}: {track['language']}")

                    while True:
                        choice = input(
                            "\nWhich subtitle track would you like to extract?"
                            " Please select a track ID or press C to cancel.\n"
                            )

                        if choice.lower() == 'c':
                            print("\nTrack selection cancelled.")
                            break

                        if not choice.isdigit():
                            print(
                                "\nInvalid input. "
                                "Please select a valid track ID number.")
                            continue

                        chosen_track = int(choice)

                        if chosen_track not in [
                            track['id'] for track in tracks
                        ]:
                            print(
                                "\nInvalid input. "
                                "Please select a valid track ID number."
                                )
                            continue

                        print(
                            f"\nProceeding with extraction of track {choice}"
                            f" from {path_input}."
                            )
                        save_file = input(
                            "\nTo save a copy of the subtitles as a .srt file,"
                            " press Y. Otherwise, "
                            "press any other key to continue: "
                            )

                        if save_file.lower() == 'y':
                            srt_name = str(path.with_suffix(".srt"))
                        else:
                            srt_name = None

                        try:
                            text = extract_text_from_mkv(
                                path_input, chosen_track, srt_name
                                )
                            file_texts.append(text)
                            print(
                                "\nText successfully extracted from"
                                f" subtitle track {choice} of {path_input}."
                                " To add text from another file "
                                "to the word list, enter another filepath."
                                )
                        except Exception as e:
                            print(f"\nSubtitle track extraction failed: {e}")
                        break

                else:
                    try:
                        text = extract_text_from_file(path_input)
                        file_texts.append(text)
                        print(
                            f"\nFile processed successfully: {path_input}."
                            "To add text from another file to the word list,"
                            " enter another filepath."
                            )
                        continue
                    except IOError as e:
                        print(
                            f"\n{e}\nValid file formats include:"
                            "\n.txt\n.srt\n.md\n.pdf\n.epub\n.mkv"
                            )
                    except Exception as e:
                        print(f"\nAn unexpected error occurred: {e}\n")

            else:
                print(
                    "\nFile not found. Please provide a valid filepath "
                    "(e.g., /path/to/input.txt)."
                    )
                time.sleep(0.5)
                continue

    if file_texts:
        combined_text = "".join(file_texts)
        print("\nText successfully extracted.")
    else:
        print("\nNo valid files were processed.")
        sys.exit()

    word_counts = generate_word_list(combined_text)

    anki_check = input(
        "\nDo you want to filter the word list "
        "using an Anki deck? (Y/n): "
        ).strip().lower()

    while True:
        if anki_check == 'y':
            decks = get_anki_decks()[1:]

            print(
                "\nWhich deck(s) would you like to filter by?"
                " Please select one or more options, separated by commas.\n")

            for i, deck in enumerate(decks, 1):
                print(f"{i}: {deck}")

            user_choice = input(
                "Enter your choice(s) or press C to cancel: "
                ).strip().lower()

            if user_choice == 'c':
                print(
                    "\nDeck selection cancelled. "
                    "Proceeding without Anki filtering."
                    )
                break

            try:
                selected_options = [
                    int(num.strip()) for num in user_choice.split(",")
                    ]

                if not all(1 <= num <= len(decks) for num in selected_options):
                    print(
                        f"\nInvalid input. "
                        f"Please enter a number between 1 and {len(decks)}."
                        )
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
                print(
                    "\nInvalid input. "
                    "Please enter one or more numbers separated by commas."
                    )
                time.sleep(0.5)
                continue
        else:
            break

    while True:
        csv_name = input(
            "\nPlease enter the destination filepath "
            "for the output CSV file, "
            "or press A to save the file in the original directory: "
            )

        if csv_name.lower() == "a" or not csv_name:
            csv_path_obj = default_dir / default_name
            break

        csv_path_obj = Path(csv_name)

        if csv_path_obj.suffix.lower() != ".csv":
            csv_path_obj = csv_path_obj.with_suffix(".csv")

        if (
            not csv_path_obj.parent.exists()
            or not csv_path_obj.parent.is_dir()
        ):
            print(
                "Invalid filepath provided. "
                "File will be saved to original directory."
                )
            csv_path_obj = default_dir / csv_path_obj.name
        break

    print('\nCreating CSV file...')

    try:
        convert_word_list_to_csv(word_counts, csv_path_obj)
    except FileNotFoundError:
        filename = Path.cwd() / csv_path_obj.name
        convert_word_list_to_csv(word_counts, filename)

    print(f"Word list file created: {csv_path_obj}")


if __name__ == '__main__':
    word_list_generator()
