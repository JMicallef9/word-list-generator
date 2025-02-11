import re

def extract_text_from_srt(filepath):
    pattern = r'\d+\s+\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\s*(.*)'

    with open(filepath) as f:
        text = f.read()
        text_lines = re.findall(pattern, text)
    
    with open(filepath, "w") as new_file:
        new_file.write('\n\n'.join(text_lines))

extract_text_from_srt('example.srt')

