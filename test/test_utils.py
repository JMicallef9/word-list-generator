from src.utils import extract_text_from_file, generate_word_list, convert_word_list_to_csv_with_translations, check_for_new_words, get_user_language, convert_word_list_to_csv
import pytest
import csv


@pytest.fixture
def example_srt(tmp_path):
    example_srt = tmp_path / 'example.srt'
    return example_srt

@pytest.fixture
def example_csv(tmp_path):
    example_csv = tmp_path / 'example.csv'
    return example_csv

@pytest.fixture
def example_text():
    example_text = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus non eros id mi volutpat faucibus. Donec id nulla non nunc iaculis egestas id vestibulum ligula. Duis auctor massa cursus volutpat venenatis. In hac habitasse platea dictumst. Aliquam sit amet laoreet dui, lobortis fermentum neque. Ut quis semper massa, a blandit quam. Duis in laoreet quam, vel facilisis orci. Aliquam at lorem non ligula gravida rhoncus. In eu suscipit lectus. Suspendisse potenti. Duis porta libero orci, id lacinia libero finibus sit amet. Donec nec magna ut ex hendrerit suscipit. In enim quam, aliquam a orci quis, volutpat vestibulum urna. Integer euismod nec diam ac congue. In sit amet sem tortor.'''
    return example_text

class TestExtractTextFromFile:
    def test_removes_timestamps(self, example_srt):
        example_srt.write_text("""1
                               00:00:35,077 --> 00:00:36,203
                               Hello!\n\n2
                               00:00:41,291 --> 00:00:42,751
                               Hello!""")
        expected = '''Hello!\n\nHello!'''
        output = extract_text_from_file(example_srt)
        assert output == expected
    
    def test_removes_italic_markers(self, example_srt):
        example_srt.write_text('''5
                               00:04:30,604 --> 00:04:32,231
                               <i>Good morning, Refiners.</i>''')
        expected = '''Good morning, Refiners.'''
        output = extract_text_from_file(example_srt)
        assert output == expected
    
    def test_handles_multiple_lines_of_text(self, example_srt):
        example_srt.write_text('''6
                                00:04:33,232 --> 00:04:36,359
                                <i>This is Mr. Milchick from work,\nand I'm thrilled to welcome you</i>''')
        expected = '''This is Mr. Milchick from work,\nand I'm thrilled to welcome you'''
        output = extract_text_from_file(example_srt)
        assert output == expected
    
    def test_removes_any_other_html_tags(self, example_srt):
        example_srt.write_text('''5
                               00:04:30,604 --> 00:04:32,231
                               <b>Good morning, Refiners.</b>''')
        expected = '''Good morning, Refiners.'''
        output = extract_text_from_file(example_srt)
        assert output == expected
    
    def test_text_unchanged_if_no_timestamps_or_html_tags(self, example_srt, example_text):
        example_srt.write_text(example_text)
        output = extract_text_from_file(example_srt)
        assert example_srt.read_text() == example_text
        assert output == example_text
    
    def test_error_message_returned_if_filepath_invalid(self):
        with pytest.raises(FileNotFoundError) as err:
            extract_text_from_file('example1.srt')
        assert str(err.value) == "Error: The file 'example1.srt' was not found."
    
    def test_IO_error_occurs_if_file_format_is_invalid(self, tmp_path):
        example_mkv = tmp_path / 'example.mkv'
        example_mkv.touch()
        with pytest.raises(IOError) as err:
            extract_text_from_file(example_mkv)
        assert str(err.value) == "Error: Could not read the file contents of 'example.mkv'. File format is invalid."

    def test_blank_document_remains_unchanged(self, example_srt):
        example_srt.touch()
        output = extract_text_from_file(example_srt)
        assert not example_srt.read_text()
        assert not output
        
class TestGenerateWordList:
    def test_empty_dict_returned_if_no_input(self):
        assert generate_word_list('') == {}

    def test_returns_dictionary(self):
        output = generate_word_list('hello')
        assert isinstance(output, dict)

    def test_counts_single_word(self):
        output = generate_word_list('hello')
        assert output == {'hello': 1}
    
    def test_counts_multiple_words(self):
        assert generate_word_list('hello world') == {'hello': 1, 'world': 1}
    
    def test_counts_multiple_instances_of_same_word(self):
        assert generate_word_list('hello world hello') == {'hello': 2, 'world': 1}

    def test_ignores_capital_letters(self):
        assert generate_word_list('Hello world hello') == {'hello': 2, 'world': 1}

    def test_filters_out_punctuation_and_lists(self):
        text = "The quick brown fox jumps over the lazy dog. The dog was not amused?"
        assert generate_word_list(text) == {'amused': 1, 'brown': 1, 'dog': 2, 'fox': 1, 'jumps': 1, 'lazy': 1, 'not': 1, 'over': 1, 'quick': 1, 'the': 3, 'was': 1}
    
    def test_filters_out_additional_punctuation_characters(self):
        text = '''¿Sueles leer antes de dormir? Al principio: <Si trabajas duro, conseguirás lo que quieres.>>'''
        assert generate_word_list(text) == {'sueles': 1, 'leer': 1, 'antes': 1, 'de': 1, 'dormir': 1, 'al': 1, 'principio': 1, 'si': 1, 'trabajas': 1, 'duro': 1, 'conseguirás': 1, 'lo': 1, 'que': 1, 'quieres': 1}
    
    def test_handles_text_in_cyrillic_script(self):
        text = 'Старик был сварливым'
        assert generate_word_list(text) == {'старик': 1, 'был': 1, 'сварливым': 1}
    
    def test_ignores_whitespace_characters(self):
        text = '''Hello\nworld\teverything\nis\tfine'''
        assert generate_word_list(text) == {'hello': 1, 'world': 1, 'everything': 1, 'is': 1, 'fine': 1}

class TestConvertToCSVWithTranslations:
    def test_creates_csv_file(self, example_csv):
        input = {'hello': 1}
        convert_word_list_to_csv_with_translations(input, example_csv, "en", "de")
        assert example_csv.exists()
    
    def test_converts_single_key_value_pair_to_csv(self, example_csv):
        input = {'hello': 1}
        convert_word_list_to_csv_with_translations(input, example_csv, "en", "de")
        with open(example_csv, newline="") as file:
            reader = csv.reader(file)
            first_row = next(reader)
            assert first_row[0] == 'hello: 1'
    
    def test_sorts_and_converts_multiple_key_value_pairs(self, example_csv):
        input = {'hello': 1, 'world': 1, 'abacus': 1}
        convert_word_list_to_csv_with_translations(input, example_csv, "en", "de")
        with open(example_csv, newline="") as file:
            reader = csv.reader(file)
            assert next(reader)[0] == 'abacus: 1'
            assert next(reader)[0] == 'hello: 1'
            assert next(reader)[0] == 'world: 1'

    def test_adds_translation_to_single_key_value_pair(self, example_csv):
        input = {'hello': 1}
        convert_word_list_to_csv_with_translations(input, example_csv, "en", "fr")
        with open(example_csv, newline="") as file:
            reader = csv.reader(file)
            first_row = next(reader)
            assert first_row[0] == 'hello: 1'
            assert first_row[1].lower() == 'bonjour'
    
    def test_adds_translations_for_multiple_words(self, example_csv):
        input = {'hello': 1, 'world': 1, 'abacus': 1}
        convert_word_list_to_csv_with_translations(input, example_csv, "en", "fr")
        with open(example_csv, newline="") as file:
            reader = csv.reader(file)
            first_row = next(reader)
            assert first_row[0] == 'abacus: 1'
            assert first_row[1].lower() == 'abaque'
            second_row = next(reader)
            assert second_row[0] == 'hello: 1'
            assert second_row[1].lower() == 'bonjour'
            third_row = next(reader)
            assert third_row[0] == 'world: 1'
            assert third_row[1].lower() == 'monde'

class TestCheckForNewWords:
    def test_returns_new_dict(self):
        input_dict = {'hello': 1}
        input_set = {'word'}
        output = check_for_new_words(input_dict, input_set)
        assert output is not input_dict
    
    def test_dict_unchanged_if_set_contains_no_matches(self):
        input_dict = {'hello': 1}
        input_set = {'word'}
        output = check_for_new_words(input_dict, input_set)
        assert output == {'hello': 1}
    
    def test_dict_item_removed_if_match_found(self):
        input_dict = {'hello': 1, 'world': 1}
        input_set = {'world'}
        assert check_for_new_words(input_dict, input_set) == {'hello': 1}

class TestGetUserLanguage:
    def test_returns_language_code_entered_by_user(self):
        assert get_user_language(['es']) == 'es'
    
    def test_returns_language_code_if_user_enters_language_name(self):
        assert get_user_language(['spanish']) == 'es'
    
    def test_ignores_capitalisation(self):
        assert get_user_language(['Spanish']) == 'es'
        assert get_user_language(['ES']) == 'es'
        assert get_user_language(['SPANISH']) == 'es'
    
    def test_handles_invalid_input_followed_by_valid_input(self, capsys):
        assert get_user_language(['invalid', 'French']) == 'fr'
        captured = capsys.readouterr()
        assert "Invalid input." in captured.out
    
    def test_available_languages_printed_upon_user_request(self, capsys):
        assert get_user_language(['l', 'French']) == 'fr'
        captured = capsys.readouterr()
        assert "Available languages: " in captured.out
        assert 'french: fr' in captured.out
        assert 'spanish: es' in captured.out
    

class TestConvertToCSV:
    def test_creates_csv_file(self, example_csv):
        input = {'hello': 1}
        convert_word_list_to_csv(input, example_csv)
        assert example_csv.exists()
    
    def test_converts_single_key_value_pair_to_csv(self, example_csv):
        input = {'hello': 1}
        convert_word_list_to_csv(input, example_csv)
        with open(example_csv, newline="") as file:
            reader = csv.reader(file)
            first_row = next(reader)
            assert first_row[0] == 'hello: 1'
    
    def test_sorts_and_converts_multiple_key_value_pairs(self, example_csv):
        input = {'hello': 1, 'world': 1, 'abacus': 1}
        convert_word_list_to_csv(input, example_csv)
        with open(example_csv, newline="") as file:
            reader = csv.reader(file)
            assert next(reader)[0] == 'abacus: 1'
            assert next(reader)[0] == 'hello: 1'
            assert next(reader)[0] == 'world: 1'

