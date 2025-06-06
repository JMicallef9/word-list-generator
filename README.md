# Word List Generator

A script that extracts all unique words from a text file or URL and saves an alphabetical list of the words to a .csv file.

Possible file formats that can be processed: .txt, .srt, .md, .docx, .pdf, .epub, .mkv

Also includes optional filtering using Anki decks.

## Requirements

- Python 3.8+
- Anki and the AnkiConnect add-on (if using Anki filtering)
- mkvtoolnix (if extracting subtitle tracks from .mkv files) 

Note: when processing .mkv files, the application requires access to `mkvmerge` for track inspection and `mkvextract` for subtitle extraction. Therefore, `mkvtoolnix` must be installed and accessible via your system's command line. Both `mkvmerge` and `mkvextract` should be available in your system's PATH. To verify this, run `mkvmerge -J` or `mkvextract --version` in your terminal. 

## Instructions

1. Clone the repository with the following command: `git clone https://github.com/JMicallef9/word-list-generator`
2. Navigate to the /src folder via the command line: `cd word-list-generator/src`
3. Create a virtual environment: `python -m venv venv` followed by `source venv/bin/activate` (macOS/Unix) OR `.venv\Scripts\activate` (Windows)
4. Install the necessary dependencies using the following command: `pip install -r requirements.txt`
5. Run the script using the following command: `python script.py`

## Running the script

You will be prompted to provide a file or link to be processed. The application handles the following inputs:

1. a URL
2. a text file in any of the following formats: .txt, .srt, .md, .docx, .pdf, .epub
3. a video file in .mkv format

When entering a file to be processed, you can provide either an absolute or relative filepath; alternatively, you can drag and drop a file into the command line.

If you provide a .mkv filepath, you will be asked to select from a list of subtitle tracks. The text from the selected subtitle track will then be used to generate a word list. The use of this feature requires both `mkvextract` and `mkvmerge` to be installed and accessible (see instructions above).

Once the file or link has been processed, you will be asked whether you wish to filter the resulting word list via Anki decks. If this option is selected, then any words appearing anywhere in a given Anki deck will be removed from the word list. To use this feature, make sure you have Anki installed and that it includes the AnkiConnect add-on. The add-on can be installed by selecting Tools > Add-ons > Browse & Install in Anki, and inputting 2055492159 in the text box labelled Code.

Finally, the script will ask for a filename and destination for the output word list file. This file will always be provided in .csv format. If no filename or destination folder is provided, a default name will be used; this will be based on the original file or URL.

## Notes

There is another script in the repository: script_with_translations.py. The purpose of this script is to provide word lists with translations in a user-specified language. This script is not yet complete and is a work in progress.