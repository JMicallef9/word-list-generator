from src.utils import extract_text_from_srt
import pytest


@pytest.fixture
def example_srt(tmp_path):
    example_srt = tmp_path / 'example.srt'
    return example_srt

class TestExtractTextFromSrt:
    def test_removes_timestamps(self, example_srt):
        example_srt.write_text('''1
                        00:00:35,077 --> 00:00:36,203
                        Hello!

                        2
                        00:00:41,291 --> 00:00:42,751
                        Hello!''')
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