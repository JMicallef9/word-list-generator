import requests
from datetime import datetime, timedelta

def get_cards_by_date(deck_name, date, side="front"):
    if side not in ("front", "back"):
        raise ValueError(
            "Invalid value: side must be either 'front' or 'back'"
            )
    
    target_date = datetime.strptime(date, '%Y-%m-%d')
    start_timestamp = int(target_date.timestamp())
    end_timestamp = int((target_date + timedelta(days=1)).timestamp())

    query = f'deck:"{deck_name}"'

    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": query
        }
    }

    response = requests.post("http://localhost:8765", json=payload).json()
    note_ids = response["result"]

    if not note_ids:
        return []
    
    payload = {
        "action": "notesInfo",
        "version": 6,
        "params": {
            "notes": note_ids
        }
    }
    response = requests.post("http://localhost:8765", json=payload).json()
    notes = response["result"]

    results = []
    for note in notes:
        mod_time = note["mod"]
        if start_timestamp <= mod_time < end_timestamp:
            fields = note["fields"]
            if side == "front":
                results.append(fields["Front"]["value"])
            elif side == "back":
                results.append(fields["Back"]["value"])

    print(f"Found {len(results)} cards modified on {date}")
    print(f"Total notes in deck: {len(note_ids)}")

    return results