from src.utils import extract_text_from_srt
import pytest


@pytest.fixture
def example_srt(tmp_path):
    example_srt = tmp_path / 'example.srt'
    example_srt.write_text('''1
                        00:00:35,077 --> 00:00:36,203
                        Hello!

                        2
                        00:00:41,291 --> 00:00:42,751
                        Hello!''')
    return example_srt

class TestExtractTextFromSrt:
    def test_removes_timestamps(self, example_srt):
        expected = '''Hello!\nHello!'''
        assert extract_text_from_srt(example_srt) == expected