from src.utils import extract_text_from_srt

class TestExtractTextFromSrt:
    def test_removes_timestamps(self):
        test_string = '''1
                        00:00:35,077 --> 00:00:36,203
                        Hello!

                        2
                        00:00:41,291 --> 00:00:42,751
                        Hello!'''
        expected = '''Hello!\nHello!'''
        assert extract_text_from_srt(test_string) == expected