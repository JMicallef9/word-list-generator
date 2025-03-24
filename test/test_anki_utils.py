import pytest
from unittest.mock import patch, MagicMock
from src.anki_utils import get_anki_decks, get_words_from_deck

@pytest.fixture
def mock_anki_post():
    with patch("requests.post") as mock_post:
        first_mock_response = MagicMock()
        first_mock_response.json.return_value = {
    "result": [1483959289817, 1483959291695],
    "error": None
}
        second_mock_response = MagicMock()
        second_mock_response.json.return_value = {
    "result": [
        {
            "noteId":1502298033753,
            "modelName": "Basic",
            "tags":["tag","another_tag"],
            "fields": {
                "Front": {"value": "front content", "order": 0},
                "Back": {"value": "back content", "order": 1}
            }
        }
    ],
    "error": None}
        mock_post.side_effect = [first_mock_response, second_mock_response]
        yield mock_post

@patch("requests.post")
class TestGetAnkiDecks:
    """Tests for fetching deck names from Anki."""

    def test_returns_list_of_decks(self, mock_post):
        """Deck names should match expected output."""
        mock_post.return_value.json.return_value = {'result': ['DeckA', 'DeckB'], 'error': None}
        output = get_anki_decks()
        assert isinstance(output, list)
        assert output == ['DeckA', 'DeckB']
    
    def test_returns_empty_list_if_no_decks(self, mock_post):
        """Should return empty list if no decks exist."""
        mock_post.return_value.json.return_value = {'result': [], 'error': None}
        output = get_anki_decks()
        assert isinstance(output, list)
        assert output == []
    
    def test_empty_list_returned_if_error_response(self, mock_post):
        """Should return empty list when Anki API returns an error."""
        mock_post.return_value.json.return_value = {'result': None, 'error': 'An error occurred.'}
        output = get_anki_decks()
        assert not output

class TestGetWordsFromDeck:
    """Tests for extracting words from an Anki deck."""

    def test_returns_set(self, mock_anki_post):
        """Output should be a set."""
        output = get_words_from_deck('deck_name')
        assert isinstance(output, set)
    
    def test_front_and_back_words_included_in_set(self, mock_anki_post):
        """Should include words from both front and back fields."""
        output = get_words_from_deck('deck_name')
        assert 'front' in output and 'back' in output
    
    def test_all_words_included_in_set(self, mock_anki_post):
        """Should include all extracted words in the output set."""
        output = get_words_from_deck('deck_name')
        assert output == {'front', 'back', 'content'}
    
    def test_capitalisation_ignored_in_output(self):
        """Should ignore capitalisation producing the output set."""
        with patch("requests.post") as mock_post:
            first_response = MagicMock()
            first_response.json.return_value = {
    "result": [1483959289817, 1483959291695],
    "error": None
} 
            second_response = MagicMock()
            second_response.json.return_value = {
    "result": [
        {
            "noteId":1502298033753,
            "modelName": "Basic",
            "tags":["tag","another_tag"],
            "fields": {
                "Front": {"value": "Hello", "order": 0},
                "Back": {"value": "hello", "order": 1}
            }
        }
    ],
    "error": None
}
            mock_post.side_effect = [first_response, second_response]
            output = get_words_from_deck('deck_name')
            assert output == {'hello'}
    
    def test_punctuation_ignored_in_output(self):
        """Should ignore punctuation when producing output set."""
        with patch("requests.post") as mock_post:
            first_response = MagicMock()
            first_response.json.return_value = {
    "result": [1483959289817, 1483959291695],
    "error": None
} 
            second_response = MagicMock()
            second_response.json.return_value = {
    "result": [
        {
            "noteId":1502298033753,
            "modelName": "Basic",
            "tags":["tag","another_tag"],
            "fields": {
                "Front": {"value": "hello: okay, everybody!", "order": 0},
                "Back": {"value": "Meaning = 'hello'", "order": 1}
            }
        }
    ],
    "error": None
}
            mock_post.side_effect = [first_response, second_response]
            output = get_words_from_deck('deck_name')
            assert output == {'hello', 'okay', 'everybody', 'meaning'}
        
    
    def test_Spanish_punctuation_ignored_in_output(self):
        """Should ignore rare or Spanish-specific punctuation in output set."""
        with patch("requests.post") as mock_post:
            first_response = MagicMock()
            first_response.json.return_value = {
    "result": [1483959289817, 1483959291695],
    "error": None
} 
            second_response = MagicMock()
            second_response.json.return_value = {
    "result": [
        {
            "noteId":1502298033753,
            "modelName": "Basic",
            "tags":["tag","another_tag"],
            "fields": {
                "Front": {"value": "¡Te lo ruego!", "order": 0},
                "Back": {"value": "¿Y tú?", "order": 1}
            }
        }
    ],
    "error": None
}
            mock_post.side_effect = [first_response, second_response]
            output = get_words_from_deck('deck_name')
            assert output == {'te', 'lo', 'ruego', 'y', 'tú'}
        
    
    def test_maintains_hyphenation_in_compound_words(self):
        """Should ensure that hyphenated words are unchanged."""
        with patch("requests.post") as mock_post:
            first_response = MagicMock()
            first_response.json.return_value = {
    "result": [1483959289817, 1483959291695],
    "error": None
} 
            second_response = MagicMock()
            second_response.json.return_value = {
    "result": [
        {
            "noteId":1502298033753,
            "modelName": "Basic",
            "tags":["tag","another_tag"],
            "fields": {
                "Front": {"value": "Físico-químico", "order": 0},
                "Back": {"value": "test", "order": 1}
            }
        }
    ],
    "error": None
}
            mock_post.side_effect = [first_response, second_response]
            output = get_words_from_deck('deck_name')
            assert output == {'físico-químico', 'test'}
        
    def test_compiles_set_from_multiple_cards(self):
        """Ensures that words from multiple Anki cards are compiled into one set."""
        with patch("requests.post") as mock_post:
            first_response = MagicMock()
            first_response.json.return_value = {
    "result": [1483959289817, 1483959291695],
    "error": None
} 
            second_response = MagicMock()
            second_response.json.return_value = {
    "result": [
        {
            "noteId":1502298033753,
            "modelName": "Basic",
            "tags":["tag","another_tag"],
            "fields": {
                "Front": {"value": "Físico-químico", "order": 0},
                "Back": {"value": "test", "order": 1}
            }
        }, {
            "noteId":1502298033753,
            "modelName": "Basic",
            "tags":["tag","another_tag"],
            "fields": {
                "Front": {"value": "front content", "order": 0},
                "Back": {"value": "back content", "order": 1}
            }
        }
    ],
    "error": None
}
            mock_post.side_effect = [first_response, second_response]
            output = get_words_from_deck('deck_name')
            assert output == {'físico-químico', 'test', 'front', 'content', 'back'}


    def test_multiple_punctuation_characters_ignored_in_output(self):
        """Ensures that all punctuation characters are omitted from output set."""
        with patch("requests.post") as mock_post:
            first_response = MagicMock()
            first_response.json.return_value = {
    "result": [1483959289817, 1483959291695],
    "error": None
} 
            second_response = MagicMock()
            second_response.json.return_value = {
    "result": [
        {
            "noteId":1502298033753,
            "modelName": "Basic",
            "tags":["tag","another_tag"],
            "fields": {
                "Front": {"value": "hello: okay!!!, everybody?!", "order": 0},
                "Back": {"value": "Meaning = 'hello'", "order": 1}
            }
        }
    ],
    "error": None
}
            mock_post.side_effect = [first_response, second_response]
            output = get_words_from_deck('deck_name')
            assert output == {'hello', 'okay', 'everybody', 'meaning'}
    

    def test_strips_out_html_tags(self):
        """Ensures that all HTML tags are stripped from extracted words."""
        with patch("requests.post") as mock_post:
            first_response = MagicMock()
            first_response.json.return_value = {
    "result": [1483959289817, 1483959291695],
    "error": None
} 
            second_response = MagicMock()
            second_response.json.return_value = {
    "result": [
        {
            "noteId":1502298033753,
            "modelName": "Basic",
            "tags":["tag","another_tag"],
            "fields": {
                "Front": {"value": "hello<br>goodbye.", "order": 0},
                "Back": {"value": "yes<br><br>no", "order": 1}
            }
        }
    ],
    "error": None
}
            mock_post.side_effect = [first_response, second_response]
            output = get_words_from_deck('deck_name')
            assert output == {'hello', 'goodbye', 'yes', 'no'}