import unittest
from page_generator import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_single_line(self):
        md = "# This is title "
        
        self.assertEqual(extract_title(md), "This is title")

    def test_multiline(self):
        md = """
# Title 2

- Item 1
- Item 2

"""

        self.assertEqual(extract_title(md), "Title 2")

    def test_incorrect1(self):
        md = """
## Wrong title

> I'm smort! :^)

"""
        with self.assertRaisesRegex(Exception, "Markdown must start with h1 header."):
            extract_title(md)


    def test_incorrect2(self):
        md = """
Normal paragrath.

# Too late for title :(

"""
        with self.assertRaisesRegex(Exception, "Markdown must start with h1 header."):
            extract_title(md)
