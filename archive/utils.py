import sqlite3
from datetime import datetime, timedelta
import html
import re


def get_anki_decks_from_sql(cursor):
    cursor.execute("SELECT name FROM decks")
    rows = cursor.fetchall()

    deck_names = [row[0] for row in rows if row[0].lower() != "default" and row[0].lower() != "all"]

    return sorted(deck_names)


def clean_text(raw_html):
    text = html.unescape(raw_html)
    clean = re.sub(r'<[^>]+>', '', text)
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

    date = datetime.strptime(date_str, "%Y-%m-%d")
    next_day = date + timedelta(days=1)

    start_ms = int(date.timestamp() * 1000)
    end_ms = int(next_day.timestamp() * 1000)

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
        fields = flds.split("\x1f")
        if side == "front":
            result.append(fields[0])
        else:
            result.append(fields[1] if len(fields) > 1 else "")


    cleaned_results = [clean_text(card) for card in result]

    return cleaned_results
