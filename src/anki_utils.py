import requests
from string import punctuation
import re


anki_connect_url = "http://localhost:8765"

def get_anki_decks():
    payload = {
        "action": "deckNames",
        "version": 6
    }
    response = requests.post(anki_connect_url, json=payload)
    return response.json().get("result", [])

def get_words_from_deck(deck_name):
    query = f'deck:"{deck_name}"'

    notes_payload = {
        "action": "findNotes",
        "version": 6,
        "params": {"query": query}
    }

    response = requests.post(anki_connect_url, json=notes_payload)
    note_ids = response.get("result", [])

    info_payload = {
        "action": "notesInfo",
        "version": 6,
        "params": {"query": note_ids}
    }

    response = requests.post(anki_connect_url, json=info_payload)
    notes = response.get("result", [])

    word_list = set()
    punc_chars = punctuation + '¿¡'

    for note in notes:
        words = note['fields']['Front']['value'].lower().split() + note['fields']['Back']['value'].lower().split()
        for word in words:
            word = re.sub(rf'^[{punc_chars}]|[{punc_chars}]$', '', word)
            if word:
                word_list.add(word)
    
    return word_list
