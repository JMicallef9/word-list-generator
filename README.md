# Word List Generator

A Python application that extracts all unique words from a text file or URL and saves an alphabetical list of the words to a `.csv` file.

The application supports the following input formats: 
- Text-based files: `.txt`, `.srt`, `.md`, `.docx`, `.pdf`, `.epub`, `.mkv`, `.ass`, `.ssa`
- URLs (web content)
- `.mkv` subtitle tracks (via subtitle extraction with `mkvtoolnix`)

The application includes optional filtering against Anki decks, and is designed to run locally or inside a Docker container.

## Instructions

### Option 1: Run locally

1. Clone the repository with the following command: `git clone https://github.com/JMicallef9/word-list-generator` (or download the repository as a ZIP package: [Download ZIP](https://github.com/JMicallef9/word-list-generator/archive/refs/heads/main.zip))
2. Navigate to the main project folder via the command line: `cd word-list-generator`
3. Create a virtual environment: `python -m venv venv` followed by `source venv/bin/activate` (macOS/Unix) OR `py -m venv venv` followed by `venv\Scripts\activate.bat` (Windows)
4. Install the necessary dependencies using the following command: `pip install -r requirements.txt`
5. Run the script using the following command: `python src/script.py`

### Option 2: Run with Docker

The app processes local files, so you must mount a directory as a volume when running the container.

1. Pull the image from DockerHub: `docker pull jmicallef9/word-list-generator:latest`
2. Run the container using `-it` and use a volume to mount the local directory containing the files you want to process e.g. `docker run --rm -it -v /Users/Username/Documents:/data jmicallef9/word-list-generator:latest`
3. Inside the container, refer to files using `/data` e.g. `/data/file_to_input.txt` 
4. Once the app has finished running, the generated `.csv` files will be accessible within the local directory given at step 2.

## Running the app

You will be prompted to provide a file or link to be processed. The application handles the following inputs:

1. a URL
2. a text file in any of the following formats: .txt, .srt, .md, .docx, .pdf, .epub
3. a video file in .mkv format

When entering a file to be processed, you can provide either an absolute or relative filepath; alternatively, you can drag and drop a file into the command line.

If you provide a .mkv filepath, you will be asked to select from a list of subtitle tracks. The text from the selected subtitle track will then be used to generate a word list.

When processing `.mkv` files, the application uses `mkvtoolnix` to extract subtitle tracks. The application only supports text-based subtitle tracks such as SRT (SubRip) or ASS/SSA (Advanced SubStation Alpha). If your `.mkv` file contains only image-based subtitles, the application will not be able to generate a word list from them.

Once the file or link has been processed, you will be asked whether you wish to filter the resulting word list via Anki decks. If this option is selected, then any words appearing anywhere in a given Anki deck will be removed from the word list. To use this feature, make sure you have Anki installed and that it includes the AnkiConnect add-on. The add-on can be installed by selecting Tools > Add-ons > Browse & Install in Anki, and inputting 2055492159 in the text box labelled Code.

Finally, the script will ask for a filename and destination for the output word list file. This file will always be provided in .csv format. If no filename or destination folder is provided, a default name will be used; this will be based on the original file or URL.

## Requirements

### Running locally
- Python 3.8+
- Python dependencies (via `pip install -r requirements.txt`)
- For optional Anki filtering:
    - [Anki](https://apps.ankiweb.net/) installed locally
    - [AnkiConnect add-on](https://ankiweb.net/shared/info/2055492159)
- Optional: MKVToolNix system install
    - This is not required when running on Windows or Linux, as executable binaries are already bundled in the project folder. However, `mkvextract` will be used automatically if installed system-wide and available in your `PATH`.
    - If running on macOS, MKVToolNix must be installed and available in your `PATH` before running the app.

### Running with Docker
- Docker - all Python dependencies and `mkvtoolnix` are included in the image.
- For optional Anki filtering:
    - Anki must still be installed and running on your host machine, with the AnkiConnect add-on enabled.
    - The container connects to Anki via the `ANKICONNECT_HOST` environment variable (default: `http://host.docker.internal:8765`)
    - If Anki is not running on the host, filtering will not be available.