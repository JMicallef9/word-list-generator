from src.anki_utils import get_anki_decks
from utils.utils import get_cards_by_date
import sys
import time


while True:

    decks = get_anki_decks()[1:]

    print("Please select a deck using the deck number:\n")

    for i, deck in enumerate(decks, 1):
        print(f"{i}: {deck}")

    user_choice = input(
        "Enter your choice or press C to cancel: "
        ).strip().lower()
    
    if user_choice == 'c':
        print(
            "\nDeck selection cancelled. Exiting application."
            )
        sys.exit()
    
    try:
        user_choice = int(user_choice.strip())

        if not 1 <= user_choice <= len(decks):
            print(
                f"\nInvalid input. "
                f"Please enter a number between 1 and {len(decks)}."
                )
            time.sleep(0.5)
            continue

    except ValueError:
        print(
            "\nInvalid input. "
            "Please enter a valid deck number."
            )
        continue

    selected = decks[user_choice - 1]

    print("You selected the following deck:\n")

    print(f"{selected}\n")

    print("\nPlease enter a date to retrieve cards from.")
    print("The date should be in the following format: 2025-07-30")
    user_date = input("Enter date here: ")

    print(f"\nRetrieving all cards from {selected} on {user_date}")

    side = input("\nTo retrieve from the back of each card, enter B: ").strip().lower()

    if side == 'b':
        side = "back"
        print(
            "\nRetrieving from the back of each card."
            )
    else:
        side = "front"
        print("\nRetrieving from the front of each card.")
    
    results = get_cards_by_date(selected, user_date, side)
    print(results)

    output_file = "anki_cards_output.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        for item in results:
            f.write(item.strip() + "\n\n")

    sys.exit()






