import unittest
import tkinter as tk
from BibleHarmony import BibleHarmonyApp
import tempfile
import os

class TestBibleHarmony(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        try:
            # Create minimal test data
            self.test_lines = [
                "INSERT INTO `verses` VALUES ('GEN', 1, 1, 'First verse');",
                "INSERT INTO `verses` VALUES ('GEN', 1, 2, 'Second verse');",
                "INSERT INTO `verses` VALUES ('REV', 22, 21, 'Last verse');"
            ]

            # Initialize app with test files
            self.app = BibleHarmonyApp(None, None)
            
            # Set up test data
            self.app.processed_lines = self.test_lines.copy()
            self.app.comparison_lines = self.test_lines.copy()
            self.app.lines_master = self.test_lines.copy()
            self.app.total_lines = len(self.test_lines)
            
            # Build verse indices
            self.app.verse_index1 = {}
            self.app.verse_index2 = {}
            for i, line in enumerate(self.test_lines):
                book, chapter, verse, _ = self.app.extract_verse_info(line)
                key = (book, str(chapter), str(verse))
                self.app.verse_index1[key] = i
                self.app.verse_index2[key] = i

        except Exception as e:
            self.fail(f"Test setup failed: {e}")

    def tearDown(self):
        """Clean up after each test."""
        self.app.destroy()

    def test_extract_verse_info(self):
        """Test verse info extraction from SQL line."""
        test_line = "INSERT INTO `verses` (`bookCode`, `chapter`, `verseNumber`, `verseText`) VALUES ('GEN', 1, 1, 'In the beginning...');"
        book, chapter, verse, text = self.app.extract_verse_info(test_line)
        
        self.assertEqual(book, 'GEN')
        self.assertEqual(chapter, '1')
        self.assertEqual(verse, '1')
        self.assertEqual(text, 'In the beginning...')

    def test_strip_strongs(self):
        """Test Strong's numbers removal."""
        test_text = "The{H1234} Lord{G5678}"
        result = self.app.strip_strongs(test_text)
        self.assertEqual(result, "The Lord")

    def test_strip_formatting(self):
        """Test formatting tags removal."""
        test_text = "<p>Text with <br> tags</p>"
        result = self.app.strip_formatting(test_text)
        self.assertEqual(result, "Text with  tags")

    def test_swap_words(self):
        """Test word substitutions."""
        test_text = "temporary-shelters"
        result = self.app.swap_words(test_text)
        self.assertEqual(result, "temporary shelters")

    def test_bible_books_order(self):
        """Test Bible books ordering."""
        self.assertEqual(self.app.BIBLE_BOOKS_ORDER['GEN'], 1)
        self.assertEqual(self.app.BIBLE_BOOKS_ORDER['REV'], 66)

    def test_read_files(self):
        """Test file reading with sample files."""
        # Create temporary test files
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("INSERT INTO `verses` VALUES ('GEN', 1, 1, 'Test verse');")
            temp_file = f.name
        
        self.app.comparison_file = temp_file
        self.app.master_file = temp_file
        
        result = self.app.read_files()
        self.assertTrue(result)
        self.assertEqual(len(self.app.comparison_lines), 1)
        
        # Clean up
        os.unlink(temp_file)

    def test_navigation(self):
        """Test verse navigation."""
        self.app.current_book = 'GEN'
        self.app.current_chapter = '1'
        self.app.current_verse = '1'
        
        # Test next/prev navigation
        self.app.next_line()
        self.assertEqual(self.app.current_verse, '2')
        
        self.app.prev_line()
        self.assertEqual(self.app.current_verse, '1')

    def test_highlight_differences(self):
        """Test difference highlighting."""
        text1 = "Sample text"
        text2 = "Sample Text"  # Capital T
        
        self.app.highlight_differences(text1, text2)
        
        # Check if case difference was highlighted
        ranges = self.app.file2_text.tag_ranges("case")
        self.assertTrue(ranges)  # Should have highlighting ranges

    def test_empty_verse_handling(self):
        """Test handling of empty verses and null values."""
        # Empty verse text
        test_line = "INSERT INTO `verses` VALUES ('GEN', 1, 1, '');"
        book, chapter, verse, text = self.app.extract_verse_info(test_line)
        self.assertEqual(text, '')
        
        # Malformed SQL line
        test_line = "INSERT INTO `verses` VALUES ('GEN', 1, 1)"
        book, chapter, verse, text = self.app.extract_verse_info(test_line)
        self.assertEqual((book, chapter, verse, text), ('', '', '', test_line))

    def test_boundary_navigation(self):
        """Test navigation at boundaries of books/chapters."""
        # Setup test data
        self.app.processed_lines = [
            "INSERT INTO `verses` VALUES ('GEN', 1, 1, 'First verse');",
            "INSERT INTO `verses` VALUES ('GEN', 1, 2, 'Second verse');",
            "INSERT INTO `verses` VALUES ('REV', 22, 21, 'Last verse');"
        ]
        self.app.total_lines = len(self.app.processed_lines)
        
        # Test at beginning of Bible
        self.app.current_line = 0
        self.app.prev_line()
        self.assertEqual(self.app.current_line, 0)  # Should stay at first verse
        
        # Test at end of Bible
        self.app.current_line = self.app.total_lines - 1
        self.app.next_line()
        self.assertEqual(self.app.current_line, self.app.total_lines - 1)  # Should stay at last verse

    def test_special_characters(self):
        """Test handling of special characters in verse text."""
        special_chars = [
            ("Quote's and \"doubles\"", "Quote's and \"doubles\""),  # Quotes
            ("Line\nbreaks\rand\tcontent", "Line breaks and content"),  # Control chars
            ("Hebrew א and Greek Ω", "Hebrew א and Greek Ω"),  # Unicode
            ("SQL injection'); DROP TABLE verses;--", "SQL injection'); DROP TABLE verses;--")  # SQL injection attempt
        ]
        
        for input_text, expected in special_chars:
            test_line = f"INSERT INTO `verses` VALUES ('GEN', 1, 1, '{input_text}');"
            _, _, _, result = self.app.extract_verse_info(test_line)
            self.assertEqual(result, input_text)

    def test_malformed_data(self):
        """Test handling of malformed input data."""
        malformed_cases = [
            "",  # Empty string
            "NOT AN SQL STATEMENT",  # Non-SQL text
            "INSERT INTO `verses` VALUES ('INVALID', 999, 999, 'text');",  # Invalid book code
            "INSERT INTO `verses` VALUES ('GEN', -1, 0, 'text');",  # Invalid chapter/verse
            None,  # None value
        ]
        
        for test_case in malformed_cases:
            try:
                book, chapter, verse, text = self.app.extract_verse_info(test_case)
                # Should return empty values for invalid input
                self.assertEqual((book, chapter, verse), ('', '', ''))
            except Exception as e:
                self.fail(f"Failed to handle malformed input: {test_case}")

    def test_concurrent_modifications(self):
        """Test handling of concurrent modifications to master text."""
        # Simulate user editing master text
        self.app.master_text.insert("1.0", "Initial text")
        
        # Simulate concurrent modifications
        def delayed_modification():
            self.app.master_text.insert("1.0", "Modified ")
        
        self.app.after(100, delayed_modification)
        self.app.store_master()  # Should handle the race condition gracefully

    def test_memory_constraints(self):
        """Test handling of large files and memory constraints."""
        # Create a large test file
        large_verse = "INSERT INTO `verses` VALUES ('GEN', 1, 1, '{}');".format("x" * 1000000)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            for _ in range(100):  # Write 100 large verses
                f.write(large_verse + "\n")
            temp_file = f.name
        
        try:
            self.app.comparison_file = temp_file
            self.app.master_file = temp_file
            result = self.app.read_files()
            self.assertTrue(result)
        finally:
            os.unlink(temp_file)

if __name__ == '__main__':
    unittest.main()