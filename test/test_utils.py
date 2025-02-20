from src.utils import extract_text_from_srt
import pytest


@pytest.fixture
def example_srt(tmp_path):
    example_srt = tmp_path / 'example.srt'
    return example_srt

@pytest.fixture
def example_text():
    example_text = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus non eros id mi volutpat faucibus. Donec id nulla non nunc iaculis egestas id vestibulum ligula. Duis auctor massa cursus volutpat venenatis. In hac habitasse platea dictumst. Aliquam sit amet laoreet dui, lobortis fermentum neque. Ut quis semper massa, a blandit quam. Duis in laoreet quam, vel facilisis orci. Aliquam at lorem non ligula gravida rhoncus. In eu suscipit lectus. Suspendisse potenti. Duis porta libero orci, id lacinia libero finibus sit amet. Donec nec magna ut ex hendrerit suscipit. In enim quam, aliquam a orci quis, volutpat vestibulum urna. Integer euismod nec diam ac congue. In sit amet sem tortor.'''
    return example_text

class TestExtractTextFromSrt:
    def test_removes_timestamps(self, example_srt):
        example_srt.write_text("""1
                               00:00:35,077 --> 00:00:36,203
                               Hello!\n\n2
                               00:00:41,291 --> 00:00:42,751
                               Hello!""")
        expected = '''Hello!\n\nHello!'''
        extract_text_from_srt(example_srt)
        assert example_srt.read_text() == expected
    
    def test_removes_italic_markers(self, example_srt):
        example_srt.write_text('''5
                               00:04:30,604 --> 00:04:32,231
                               <i>Good morning, Refiners.</i>''')
        expected = '''Good morning, Refiners.'''
        extract_text_from_srt(example_srt)
        assert example_srt.read_text() == expected
    
    def test_handles_multiple_lines_of_text(self, example_srt):
        example_srt.write_text('''6
                                00:04:33,232 --> 00:04:36,359
                                <i>This is Mr. Milchick from work,\nand I'm thrilled to welcome you</i>''')
        expected = '''This is Mr. Milchick from work,\nand I'm thrilled to welcome you'''
        extract_text_from_srt(example_srt)
        assert example_srt.read_text() == expected
    
    def test_removes_any_other_html_tags(self, example_srt):
        example_srt.write_text('''5
                               00:04:30,604 --> 00:04:32,231
                               <b>Good morning, Refiners.</b>''')
        expected = '''Good morning, Refiners.'''
        extract_text_from_srt(example_srt)
        assert example_srt.read_text() == expected
    
    def test_text_unchanged_if_no_timestamps_or_html_tags(self, example_srt, example_text):
        example_srt.write_text(example_text)
        extract_text_from_srt(example_srt)
        assert example_srt.read_text() == example_text
    
    def test_error_message_returned_if_filepath_invalid(self):
        with pytest.raises(FileNotFoundError) as err:
            extract_text_from_srt('example1.srt')
        assert str(err.value) == "Error: The file 'example1.srt' was not found."
    
    def test_IO_error_occurs_if_file_format_is_invalid(self, tmp_path):
        example_mkv = tmp_path / 'example.mkv'
        example_mkv.touch()
        with pytest.raises(IOError) as err:
            extract_text_from_srt(example_mkv)
        assert str(err.value) == "Error: Could not read the file contents of 'example.mkv'. File format is invalid."

        





