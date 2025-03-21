# Word List Generator

A script that extracts all unique words from a text file and saves an alphabetical list of the words to a .csv file.

Possible file formats that can be processed: .txt, .srt & .md

Also includes optional filtering using Anki decks.

## Requirements

- Python 3.8+
- Anki and the AnkiConnect add-on (if using Anki filtering)

## Instructions

1. Download the /src folder.
2. Navigate to the /src folder via the command line.
3. Install the necessary dependencies using the following command: pip install -r requirements.txt
4. Run the script using the following command: python script.py

## Running the script

You will be prompted to provide a file to be processed. You can enter either an absolute or relative filepath; alternatively, you can drag and drop a file into the command line.

The script will ask you whether you want to filter the resulting word list via Anki decks. If this option is selected, then any words appearing anywhere in a given Anki deck will be removed from the word list. To use this feature, make sure you have Anki installed and that it includes the AnkiConnect add-on. The add-on can be installed by selecting Tools > Add-ons > Browse & Install in Anki, and inputting 2055492159 in the text box labelled Code.

Finally, the script will ask for a filename for the output word list file. This file will always be provided in .csv format.