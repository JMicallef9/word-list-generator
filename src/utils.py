import re

def extract_text_from_srt(filepath):
    timestamp_pattern = r'\d+\s+\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\s*(.*)'
    italic_pattern = r'<(/?i)>'

    with open(filepath) as f:
        text = f.read()
    
    text_lines = re.findall(timestamp_pattern, text)
    cleaned_text = '\n\n'.join(text_lines)
    cleaned_text = re.sub(italic_pattern, "", cleaned_text)

    with open(filepath, "w") as new_file:
        new_file.write(cleaned_text)

extract_text_from_srt('example.srt')

