import sqlite3
from datetime import datetime, timedelta
import html
import re


def get_anki_decks_from_sql(cursor):
    cursor.execute("SELECT name FROM decks")
    rows = cursor.fetchall()

    # Filter out "Default" and anything you don't want
    deck_names = [row[0] for row in rows if row[0].lower() != "default" and row[0].lower() != "all"]

    return sorted(deck_names)


# def get_cards_by_date(deck_name, date, side="front"):
#     if side not in ("front", "back"):
#         raise ValueError(
#             "Invalid value: side must be either 'front' or 'back'"
#             )
    
#     target_date = datetime.strptime(date, '%Y-%m-%d')
#     start_timestamp = int(target_date.timestamp())
#     end_timestamp = int((target_date + timedelta(days=1)).timestamp())

#     query = f'deck:"{deck_name}"'

#     payload = {
#         "action": "findNotes",
#         "version": 6,
#         "params": {
#             "query": query
#         }
#     }

#     response = requests.post("http://localhost:8765", json=payload).json()
#     note_ids = response["result"]

#     if not note_ids:
#         return []
    
#     payload = {
#         "action": "notesInfo",
#         "version": 6,
#         "params": {
#             "notes": note_ids
#         }
#     }
#     response = requests.post("http://localhost:8765", json=payload).json()
#     notes = response["result"]

#     results = []
#     for note in notes:
#         mod_time = note["mod"]
#         if start_timestamp <= mod_time < end_timestamp:
#             fields = note["fields"]
#             if side == "front":
#                 results.append(fields["Front"]["value"])
#             elif side == "back":
#                 results.append(fields["Back"]["value"])

#     print(f"Found {len(results)} cards modified on {date}")
#     print(f"Total notes in deck: {len(note_ids)}")

#     return results




# cursor.execute("SELECT name, id FROM decks")
# print(cursor.fetchall())


def clean_text(raw_html):
    # First, unescape HTML entities like &nbsp;, &amp;, etc.
    text = html.unescape(raw_html)
    # Then, remove any remaining HTML tags like <b>, </b>, etc.
    clean = re.sub(r'<[^>]+>', '', text)
    # Optionally, you can strip leading/trailing whitespace
    return clean.strip()

def get_deck_id(cursor, deck_name):
    cursor.execute("SELECT id FROM decks WHERE name = ? COLLATE NOCASE", (deck_name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        raise ValueError(f"Deck '{deck_name}' not found")


def get_cards_by_creation_date(cursor, deck_id, date_str, side="front"):
    assert side in ("front", "back"), "side must be 'front' or 'back'"

    # Convert date string to datetime and calculate timestamps in milliseconds
    date = datetime.strptime(date_str, "%Y-%m-%d")
    next_day = date + timedelta(days=1)

    start_ms = int(date.timestamp() * 1000)
    end_ms = int(next_day.timestamp() * 1000)

    # Query cards created in this deck within the date range
    cursor.execute("""
        SELECT n.flds
        FROM cards c
        JOIN notes n ON c.nid = n.id
        WHERE c.did = ?
          AND c.id BETWEEN ? AND ?
    """, (deck_id, start_ms, end_ms))

    rows = cursor.fetchall()

    result = []
    for (flds,) in rows:
        fields = flds.split("\x1f")  # Anki separates note fields with ASCII 31
        if side == "front":
            result.append(fields[0])
        else:
            result.append(fields[1] if len(fields) > 1 else "")


    cleaned_results = [clean_text(card) for card in result]

    return cleaned_results

# deck_id = get_deck_id(cursor, "ru_words")

# cards_front = get_cards_by_creation_date(deck_id, "2025-02-11", side="front")

# print(f"Cards created on 2025-02-11 in deck 'ru_words':")
# for card in cards_front:
#     print(card)