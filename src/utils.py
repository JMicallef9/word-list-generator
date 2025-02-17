import re

def extract_text_from_srt(filepath):
    timestamp_pattern = r'\d+\s+\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\s*'
    italic_pattern = r'<(/?i)>'

    with open(filepath) as f:
        text = f.read()
    
    cleaned_text = re.sub(timestamp_pattern, "", text)
    cleaned_text = re.sub(italic_pattern, "", cleaned_text)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

# extract_text_from_srt('example.srt')

