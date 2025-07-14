import requests
from string import punctuation
import re
import html
import os


def get_anki_connect_url():
    """
    Retrieves Ankiconnect URL as environment variable or default value.

    Args:
        None.

    Returns:
        str: The Ankiconnect URL.
    """
    return os.getenv("ANKICONNECT_HOST", "http://localhost:8765")


def get_anki_decks():
    """
    Returns a list of the user's Anki decks.

    Args:
        None.

    Returns:
        list: The names of all decks in the user's Anki collection.
    """
    anki_connect_url = get_anki_connect_url()

    payload = {
        "action": "deckNames",
        "version": 6
    }
    response = requests.post(anki_connect_url, json=payload, timeout=5)
    return response.json().get("result", [])


def get_words_from_deck(deck_name):
    """
    Retrieves all the unique words that appear in an Anki deck.

    Args:
        deck_name (str): The name of an Anki deck.

    Returns:
        set: All unique words appearing in cards from the given deck.
    """
    anki_connect_url = get_anki_connect_url()

    query = f'deck:"{deck_name}"'

    notes_payload = {
        "action": "findNotes",
        "version": 6,
        "params": {"query": query}
    }

    response = requests.post(anki_connect_url, json=notes_payload, timeout=5)
    response_json = response.json()
    note_ids = response_json.get("result", [])

    info_payload = {
        "action": "notesInfo",
        "version": 6,
        "params": {"notes": note_ids}
    }

    response = requests.post(anki_connect_url, json=info_payload, timeout=5)
    response_json = response.json()
    notes = response_json.get("result", [])

    word_list = set()
    punc_chars = punctuation + '¿¡♪'

    for note in notes:
        front = note['fields']['Front']['value'].lower()
        back = note['fields']['Back']['value'].lower()
        word_string = front + ' ' + back

        word_string = re.sub(r'<[^>]+>', ' ', word_string)
        word_string = html.unescape(word_string)

        words = re.findall(r'\b\w[\w\'-]*\b', word_string)

        for word in words:
            word = re.sub(rf'^[{punc_chars}]*|[{punc_chars}]*$', '', word)
            if word:
                word_list.add(word)

    return word_list
