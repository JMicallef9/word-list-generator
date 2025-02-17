import re

def extract_text_from_srt(filepath):
    timestamp_pattern = r'\d+\s+\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\s*'
    tag_pattern = r'<.*?>'
    combined_pattern = rf"{timestamp_pattern}|{tag_pattern}"

    with open(filepath) as f:
        text = f.read()
    
    cleaned_text = re.sub(combined_pattern, "", text)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

# extract_text_from_srt('example.srt')

