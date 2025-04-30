"""
TODO List:
1. Incorporate stripStrongs_bibleVerses_GUI functionality:
   - Add Strong's number stripping
   - Merge GUI elements from stripStrongs
   - Keep verse text comparison features

   selecting use file 1 or 2 to add back stripped sql stuff
   editable text boxes
    - Add button to strip Strong's numbers
    - Add toggle to hide identical lines

2. Add master file handling:
   - Add third file panel for master reference
   - Implement verse comparison against master
   - Add master file selection controls
   - Update merge logic to handle master file

3. Improve GUI layout:
   - Add LabelFrame widgets around file sections
   - Group navigation controls in frame
   - Add frame around merge controls
   - Better visual separation of components

4. Future Enhancements:
   - Add configuration for default paths
   - Save/restore last used settings
"""

PADDING = 10
TEXT_HEIGHT = 5
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 400
COMMON_PREFIX = "INSERT INTO `verses` (`bookCode`, `chapter`, `verseNumber`, `verseText`) VALUES ("
COMMON_SUFFIX = ");"
ENCODING = "utf-8"
ERRORS_POLICY = "replace"
INSERT_KEYWORD = "INSERT INTO"
NO_FILE_MSG = "No file selected"
VERSE_REGEX = r"\('(\w+)',\s*(\d+),\s*(\d+),\s*'(.+)'\)"

import re
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import difflib  # Add this import to use difflib for highlighting differences

HIGHLIGHT_COLORS = {
    "case": "#90EE90",         # Light green
    "punctuation": "#FFFF00",  # Bright yellow
    "other": "#FFB6C1",        # Light pink
}

# Update the BIBLE_BOOKS_ORDER constant with traditional ordering
BIBLE_BOOKS_ORDER = {
    'GEN':  1, 'EXO':  2, 'LEV':  3, 'NUM':  4, 'DEU':  5,
    'JOS':  6, 'JDG':  7, 'RUT':  8, '1SA':  9, '2SA': 10,
    '1KI': 11, '2KI': 12, '1CH': 13, '2CH': 14, 'EZR': 15,
    'NEH': 16, 'EST': 17, 'JOB': 18, 'PSA': 19, 'PRO': 20,
    'ECC': 21, 'SNG': 22, 'ISA': 23, 'JER': 24, 'LAM': 25,
    'EZK': 26, 'DAN': 27, 'HOS': 28, 'JOL': 29, 'AMO': 30,
    'OBA': 31, 'JON': 32, 'MIC': 33, 'NAH': 34, 'HAB': 35,
    'ZEP': 36, 'HAG': 37, 'ZEC': 38, 'MAL': 39,
    'MAT': 40, 'MRK': 41, 'LUK': 42, 'JHN': 43, 'ACT': 44,
    'ROM': 45, '1CO': 46, '2CO': 47, 'GAL': 48, 'EPH': 49,
    'PHP': 50, 'COL': 51, '1TH': 52, '2TH': 53, '1TI': 54,
    '2TI': 55, 'TIT': 56, 'PHM': 57, 'HEB': 58, 'JAS': 59,
    '1PE': 60, '2PE': 61, '1JN': 62, '2JN': 63, '3JN': 64,
    'JUD': 65, 'REV': 66,

    # my alternate codes!
    '1SM':  9,  # 1 Samuel
    '2SM': 10,  # 2 Samuel
    'SON': 22,  # Song of Songs
    'EZE': 26,  # Ezekiel
    'JOE': 29,  # Joel
    'MAR': 41,  # Mark
    'JOH': 43,  # John
    'JAM': 59,  # James
    '1JO': 62,  # 1 John
    '2JO': 63,  # 2 John
    '3JO': 64,  # 3 John
    'JDE': 65,  # Jude

    # Other alternate codes
    'PSL': 19,  # Psalms
    'SON': 22,  # Song of Solomon
    'EZE': 26,  # Ezekiel
    'NAM': 34,  # Nahum
    'JHO': 43,  # John
    'PHI': 50  # Philippians
}

class BibleHarmonyApp(tk.Tk):
    """A tkinter application for comparing and editing Bible verse files."""

    def __init__(self, file1, file2):
        """Initialize the application with two files to compare.

        Args:
            file1 (str): Path to the first file
            file2 (str): Path to the second file
        """
        super().__init__()

        self.title("BibleHarmony")  # Set the window title
        self.file1 = file1
        self.file2 = file2
        self.current_line = 0
        self.total_lines = 0
        self.merged_lines = []
        # Add these lines to initialize the line lists
        self.lines1 = []
        self.lines2 = []
        
        # Set a minimum size for the window
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Configure the grid to allow column expansion
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Navigation Frame
        nav_frame = tk.Frame(self)
        nav_frame.grid(row=0, column=0, columnspan=2, sticky="EW", padx=PADDING)

        # Book navigation
        tk.Label(nav_frame, text="Book:").pack(side="left", padx=2)
        self.book_combo = ttk.Combobox(nav_frame, width=5)
        self.book_combo.pack(side="left", padx=2)
        self.prev_B_button = tk.Button(nav_frame, text="Prev B", command=self.prev_book)
        self.prev_B_button.pack(side="left", padx=2)
        self.next_B_button = tk.Button(nav_frame, text="Next B", command=self.next_book)
        self.next_B_button.pack(side="left", padx=2)

        tk.Label(nav_frame, text="Chapter:").pack(side="left", padx=2)
        self.chapter_combo = ttk.Combobox(nav_frame, width=3)
        self.chapter_combo.pack(side="left", padx=2)
        self.prev_c_button = tk.Button(nav_frame, text="Prev C", command=self.prev_chapter)
        self.prev_c_button.pack(side="left", padx=2)
        self.next_button = tk.Button(nav_frame, text="Next C", command=self.next_chapter)
        self.next_button.pack(side="left", padx=2)


        tk.Label(nav_frame, text="Verse:").pack(side="left", padx=2)
        self.verse_combo = ttk.Combobox(nav_frame, width=3)
        self.verse_combo.pack(side="left", padx=2)

        self.prev_button = tk.Button(nav_frame, text="Prev", command=self.prev_line)
        self.prev_button.pack(side="left", padx=2)

        self.next_button = tk.Button(nav_frame, text="Next", command=self.next_line)
        self.next_button.pack(side="left", padx=2)

        # File 1 Text Field
        file1_frame = tk.Frame(self)
        file1_frame.grid(row=1, column=0, columnspan=2, sticky="EW", padx=PADDING, pady=PADDING)
        self.file1_label = tk.Label(file1_frame, text="File 1")
        self.file1_label.pack(side="left")
        self.file1_button = tk.Button(file1_frame, text="Select File", command=self.select_file1)
        self.file1_button.pack(side="right")

        self.file1_name_label = tk.Label(self, text=NO_FILE_MSG, anchor="w")
        self.file1_name_label.grid(row=2, column=0, columnspan=2, sticky="EW", padx=PADDING)

        self.file1_text = tk.Text(self, height=TEXT_HEIGHT, wrap="word", state="disabled")
        self.file1_text.grid(row=3, column=0, columnspan=2, padx=PADDING, pady=5, sticky="EW")

        # File 2 Text Field
        self.file2_label = tk.Label(self, text="File 2")
        self.file2_label.grid(row=4, column=0, sticky="W", padx=PADDING)
        self.file2_button = tk.Button(self, text="Select File", command=self.select_file2)
        self.file2_button.grid(row=4, column=1, padx=PADDING, sticky="E")
        self.file2_name_label = tk.Label(self, text=NO_FILE_MSG, anchor="w")
        self.file2_name_label.grid(row=5, column=0, columnspan=2, sticky="EW", padx=PADDING)

        self.file2_text = tk.Text(self, height=TEXT_HEIGHT, wrap="word", state="disabled")
        self.file2_text.grid(row=6, column=0, columnspan=2, padx=PADDING, pady=5, sticky="EW")

        # Selected Line Text Field
        self.selected_label = tk.Label(self, text="Selected Line")
        self.selected_label.grid(row=7, column=0, sticky="W", padx=PADDING)
        self.selected_text = tk.Text(self, height=TEXT_HEIGHT, wrap="word", state="disabled")
        self.selected_text.grid(row=8, column=0, columnspan=2, padx=PADDING, pady=5, sticky="EW")

        # Buttons
        self.merge_button = tk.Button(self, text="Merge", command=self.merge_line)
        self.merge_button.grid(row=9, column=0, sticky="", padx=PADDING, pady=10)

        self.use_file1_button = tk.Button(self, text="Use File 1", command=self.use_file1)
        self.use_file1_button.grid(row=10, column=0, sticky="W", padx=PADDING, pady=5)

        self.use_file2_button = tk.Button(self, text="Use File 2", command=self.use_file2)
        self.use_file2_button.grid(row=10, column=1, sticky="E", padx=PADDING, pady=5)

        # Status Bar
        self.status_bar = tk.Label(self, text="Line 1 of 100", anchor="w")
        self.status_bar.grid(row=11, column=0, columnspan=2, sticky="EW", padx=10, pady=5)

        # Show the first line
        self.show_line()

        self.bind("<Return>", lambda event: self.merge_line())
        self.bind("Control-1", lambda event: self.use_file1())
        self.bind("Control-2", lambda event: self.use_file2())
        self.bind("<Control-s>", lambda event: self.merge_line())
        self.bind("<Control-Left>", lambda event: self.prev_line())
        self.bind("<Control-Right>", lambda event: self.next_line())
        self.bind("<Control-Up>", lambda event: self.prev_chapter())
        self.bind("<Control-Down>", lambda event: self.next_chapter())

        # Automate lookup from book, chapter & verse combos
        self.book_combo.bind('<<ComboboxSelected>>', lambda e: self.navigate_to_verse())
        self.chapter_combo.bind('<<ComboboxSelected>>', lambda e: self.navigate_to_verse())
        self.verse_combo.bind('<<ComboboxSelected>>', lambda e: self.navigate_to_verse())

    def select_file(self, file_number):
        """Open a file dialog to select a file and update the display.
        
        Args:
            file_number (int): The file number (1 or 2) to select
        """
        file_path = filedialog.askopenfilename(title=f"Select File {file_number}")
        if file_path:
            try:
                with open(file_path, "r", encoding=ENCODING, errors=ERRORS_POLICY):
                    if file_number == 1:
                        self.file1 = file_path
                        self.file1_name_label.config(text=file_path)
                    else:
                        self.file2 = file_path
                        self.file2_name_label.config(text=file_path)
                    
                    self.read_files()
                    self.filter_and_validate_lines()
                    self.current_line = 0
                    self.show_line()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to open File {file_number}: {e}")

    def select_file1(self):
        """Open a file dialog to select the first file."""
        self.select_file(1)

    def select_file2(self):
        """Open a file dialog to select the second file."""
        self.select_file(2)

    def read_and_filter_lines(self, file_path):
        """Read lines from a file and filter for INSERT INTO statements.

        Args:
            file_path (str): Path to the file to read

        Returns:
            list: Filtered lines containing INSERT INTO statements
        """
        try:
            with open(file_path, "r", encoding=ENCODING, errors=ERRORS_POLICY) as f:
                lines = f.readlines()
            return [line for line in lines if INSERT_KEYWORD in line]
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to read file: {e}")
            return []

    def show_line(self):
        """Display the current line from both files and highlight differences."""
        try:
            line1, line2 = self.get_current_lines()
            self.update_text_field(self.file1_text, line1)
            self.update_text_field(self.file2_text, line2)
            self.highlight_differences(line1, line2)
            self.update_selected_text(line1, line2)
            self.update_status()
            self.update_navigation_options()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to process files: {e}")

    def read_files(self):
        """Read the contents of both input files into memory."""
        app.file1_name_label.config(text=default_file1)
        app.file2_name_label.config(text=default_file2)
        try:
            if not self.file1 or not self.file2:
                tk.messagebox.showerror("Error", "Both file paths must be selected before reading files.")
                return False

            with open(self.file1, "r", encoding=ENCODING, errors=ERRORS_POLICY) as f1:
                self.lines1 = [line for line in f1 if INSERT_KEYWORD in line]
            with open(self.file2, "r", encoding=ENCODING, errors=ERRORS_POLICY) as f2:
                self.lines2 = [line for line in f2 if INSERT_KEYWORD in line]
            return True
        except Exception as e:
        # Reset labels if file loading fails
            app.file1_name_label.config(text=NO_FILE_MSG)
            app.file2_name_label.config(text=NO_FILE_MSG)
            tk.messagebox.showerror("Error", f"Failed to read files: {e}")
            return False

    def filter_and_validate_lines(self):
        """Filter lines for SQL statements and ensure verses are aligned between files."""
        # First filter for SQL statements
        self.lines1 = self.filter_lines(self.lines1)
        self.lines2 = self.filter_lines(self.lines2)

        # Create dictionaries to map (book, chapter, verse) to line content
        verses1 = {}
        verses2 = {}
        
        # Process file 1
        for line in self.lines1:
            book, chapter, verse, _ = self.extract_verse_info(line)
            if book and chapter and verse:
                key = (book, int(chapter), int(verse))
                verses1[key] = line
                
        # Process file 2
        for line in self.lines2:
            book, chapter, verse, _ = self.extract_verse_info(line)
            if book and chapter and verse:
                key = (book, int(chapter), int(verse))
                verses2[key] = line

        # Get all verse references in Bible order
        def verse_key(verse_tuple):
            book, chapter, verse = verse_tuple
            return (BIBLE_BOOKS_ORDER.get(book, 999), int(chapter), int(verse))

        all_verses = sorted(set(verses1.keys()) | set(verses2.keys()), key=verse_key)
        
        # Rebuild lines with empty placeholders for missing verses
        self.lines1 = []
        self.lines2 = []
        empty_line = f"{COMMON_PREFIX}'',0,0,''{COMMON_SUFFIX}\n"
        
        for verse_key in all_verses:
            self.lines1.append(verses1.get(verse_key, empty_line))
            self.lines2.append(verses2.get(verse_key, empty_line))

        self.total_lines = len(all_verses)
        self.current_line = max(0, min(self.current_line, self.total_lines - 1))

    def get_current_lines(self):
        """Get the current line from both files with metadata stripped."""
        # Get raw lines first
        raw_line1 = self.lines1[self.current_line] if self.current_line < len(self.lines1) else ""
        raw_line2 = self.lines2[self.current_line] if self.current_line < len(self.lines2) else ""

        # Update verse info display based on selected file or default to file1
        if (self.current_line, 2) in self.merged_lines and raw_line2:
            # Use file2's verse info if it's selected
            book, chapter, verse, text2 = self.extract_verse_info(raw_line2)
            self.update_verse_display(book, chapter, verse)
            _, _, _, text1 = self.extract_verse_info(raw_line1) if raw_line1 else ("", "", "", "")
            return text1, text2
        elif raw_line1:
            # Default to file1's verse info
            book, chapter, verse, text1 = self.extract_verse_info(raw_line1)
            self.update_verse_display(book, chapter, verse)
            _, _, _, text2 = self.extract_verse_info(raw_line2) if raw_line2 else ("", "", "", "")
            return text1, text2
        else:
            # Clear comboboxes if no valid lines
            self.update_verse_display("", "", "")
            return ("File 1 is empty or contains no valid lines.", 
                    "File 2 is empty or contains no valid lines.")

    def update_verse_display(self, book, chapter, verse):
        """Update the verse navigation comboboxes to show current verse.
        
        Args:
            book (str): Book code
            chapter (str): Chapter number
            verse (str): Verse number
        """
        if book and chapter and verse:
            self.book_combo.set(book)
            self.chapter_combo.set(chapter)
            self.verse_combo.set(verse)
            self.update_navigation_options()
        else:
            self.book_combo.set('')
            self.chapter_combo.set('')
            self.verse_combo.set('')

    def highlight_differences(self, line1, line2):
        """Highlight differences between two lines using different colors.

        Args:
            line1 (str): Line from first file
            line2 (str): Line from second file
        """
        # Clear all existing highlights
        self.file1_text.tag_delete("case", "punctuation", "other")
        self.file2_text.tag_delete("case", "punctuation", "other")

        matcher = difflib.SequenceMatcher(None, line1, line2)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag in ("replace", "insert", "delete"):
                # First, check for exact differences
                if line1[i1:i2] == line2[j1:j2]:
                    continue  # Skip if the text is identical
                    
                # Check for case differences only
                if line1[i1:i2].lower() == line2[j1:j2].lower():
                    self.apply_highlight("case", i1, i2, j1, j2)
                    continue

                # Check for punctuation differences only
                stripped_line1 = line1[i1:i2].translate(str.maketrans("", "", ".,!?:;"))
                stripped_line2 = line2[j1:j2].translate(str.maketrans("", "", ".,!?:;"))
                if stripped_line1.lower() == stripped_line2.lower():
                    self.apply_highlight("punctuation", i1, i2, j1, j2)
                    continue

                # If neither case nor punctuation, mark as other
                self.apply_highlight("other", i1, i2, j1, j2)

    def apply_highlight(self, highlight_type, i1, i2, j1, j2):
        """Apply a highlight of specified type to regions in both text widgets.

        Args:
            highlight_type (str): Type of highlight ("case", "punctuation", or "other")
            i1 (int): Start index in first line
            i2 (int): End index in first line
            j1 (int): Start index in second line
            j2 (int): End index in second line
        """
        # Apply the highlight using a specific tag for the type
        self.file1_text.tag_add(highlight_type, f"1.{i1}", f"1.{i2}")
        self.file2_text.tag_add(highlight_type, f"1.{j1}", f"1.{j2}")
        self.file1_text.tag_config(highlight_type, background=HIGHLIGHT_COLORS[highlight_type])
        self.file2_text.tag_config(highlight_type, background=HIGHLIGHT_COLORS[highlight_type])

    def update_selected_text(self, line1, line2):
        """Update the selected text field based on user's choice.

        Args:
            line1 (str): Line from first file
            line2 (str): Line from second file
        """
        self.selected_text.config(state="normal")
        self.selected_text.delete(1.0, tk.END)
        if (self.current_line, 1) in self.merged_lines:
            self.selected_text.insert(tk.END, line1)
        elif (self.current_line, 2) in self.merged_lines:
            self.selected_text.insert(tk.END, line2)
        self.selected_text.config(state="disabled")

    def update_text_field(self, text_widget, content):
        """Update a text widget with new content.

        Args:
            text_widget (tk.Text): Text widget to update
            content (str): New content to display
        """
        text_widget.config(state="normal")
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, content)
        text_widget.config(state="disabled")

    def update_status(self):
        """Update the status bar with current line numbers and file statistics."""
        current_book = self.book_combo.get() or "?"
        current_chapter = self.chapter_combo.get() or "?"
        current_verse = self.verse_combo.get() or "?"
        self.status_bar.config(
            text=f"{current_book} {current_chapter}:{current_verse} | "
                 f"Line {self.current_line + 1} of {self.total_lines} | "
                 f"File 1: {len(self.lines1)} lines, File 2: {len(self.lines2)} lines"
        )

    def use_file(self, source):
        """Mark the current line as selected from specified source and preserve SQL structure.

        Args:
            source (int): Source identifier (1 for file1, 2 for file2)
        """
        # Get the raw line from the appropriate file
        raw_line = self.lines2[self.current_line] if source == 2 else self.lines1[self.current_line]
        clean_line = raw_line.strip()
        
        # Remove any existing COMMON_PREFIX and COMMON_SUFFIX if present
        if clean_line.startswith(COMMON_PREFIX):
            clean_line = clean_line[len(COMMON_PREFIX):]
        if clean_line.endswith(COMMON_SUFFIX):
            clean_line = clean_line[:-len(COMMON_SUFFIX)]
            
        # Reconstruct the full SQL line by reattaching prefix and suffix
        full_sql_line = f"{COMMON_PREFIX}{clean_line}{COMMON_SUFFIX}"
        
        # Remove any existing selection for the current line
        self.merged_lines = [(line, src) for line, src in self.merged_lines if line != self.current_line]
        
        # Add the new selection with the full SQL line
        self.merged_lines.append((self.current_line, source))
        
        # Update selected text to show full SQL
        self.selected_text.config(state="normal")
        self.selected_text.delete(1.0, tk.END)
        self.selected_text.insert(tk.END, full_sql_line)
        self.selected_text.config(state="disabled")
        
        self.show_line()

    def use_file1(self):
        """Select the current line from file 1."""
        self.use_file(1)

    def use_file2(self):
        """Select the current line from file 2."""
        self.use_file(2)

    def navigate_book(self, direction):
        """Move to the next or previous book if available.
        
        Args:
            direction (int): 1 for next book, -1 for previous book
        """
        current_book = self.book_combo.get()
        if not current_book:
            return

        # Get current book's order
        current_order = BIBLE_BOOKS_ORDER.get(current_book, 999)
        
        # Get available books and their order numbers
        available_books = self.get_available_books()
        book_orders = {book: BIBLE_BOOKS_ORDER.get(book, 999) 
                      for book in available_books}
        
        # Find next/prev book based on Bible order
        target_book = None
        if direction > 0:  # Next book
            next_books = [(order, book) for book, order in book_orders.items() 
                         if order > current_order]
            if next_books:
                target_book = min(next_books)[1]
        else:  # Previous book
            prev_books = [(order, book) for book, order in book_orders.items() 
                         if order < current_order]
            if prev_books:
                target_book = max(prev_books)[1]
        
        if target_book:
            self.book_combo.set(target_book)
            # Set to first chapter of new book
            chapters = sorted(self.get_available_chapters(target_book), key=int)
            if chapters:
                self.chapter_combo.set(chapters[0])
                # Set to first verse of new chapter
                verses = sorted(self.get_available_verses(target_book, chapters[0]), key=int)
                if verses:
                    self.verse_combo.set(verses[0])
                    self.navigate_to_verse()

    def next_book(self):
        """Move to the next book if available."""
        self.navigate_book(1)

    def prev_book(self):
        """Move to the previous book if available."""
        self.navigate_book(-1)

    def navigate_chapter(self, direction):
        """Move to the next or previous chapter if available.
        
        Args:
            direction (int): 1 for next chapter, -1 for previous chapter
        """
        current_book = self.book_combo.get()
        current_chapter = self.chapter_combo.get()
        
        if not current_book or not current_chapter:
            return
            
        # Get all chapters for current book
        chapters = sorted(self.get_available_chapters(current_book), key=int)
        
        try:
            current_index = chapters.index(current_chapter)
            if ((direction > 0 and current_index < len(chapters) - 1) or 
                (direction < 0 and current_index > 0)):
                # Move to next/previous chapter
                target_chapter = chapters[current_index + direction]
                self.chapter_combo.set(target_chapter)
                # Set to first verse of new chapter
                verses = sorted(self.get_available_verses(current_book, target_chapter), key=int)
                if verses:
                    self.verse_combo.set(verses[0])
                    self.navigate_to_verse()
        except ValueError:
            pass

    def next_chapter(self):
        """Move to the next chapter if available."""
        self.navigate_chapter(1)

    def prev_chapter(self):
        """Move to the previous chapter if available."""
        self.navigate_chapter(-1)

    def prev_line(self):
        """Move to the previous line if available."""
        if self.current_line > 0:
            self.current_line -= 1
        self.show_line()

    def next_line(self):
        """Move to the next line if available."""
        if self.current_line < self.total_lines - 1:
            self.current_line += 1
        self.show_line()

    def merge_line(self):
        """Save the merged file with user selections."""
        output_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Merged File")
        if not output_path:
            return  # User canceled the save dialog

        try:
            with open(output_path, "w") as outfile:
                self.write_merged_lines(outfile)
            tk.messagebox.showinfo("Success", f"Merged file saved to {output_path}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save merged file: {e}")

    def write_merged_lines(self, outfile):
        """Write the merged lines to the output file.

        Args:
            outfile (file): Open file object to write to
        """
        # Ensure selections are sorted by line number
        self.merged_lines.sort(key=lambda x: x[0])
        selected_lines = {line: source for line, source in self.merged_lines}

        for i in range(self.total_lines):
            line = self.get_line_to_write(i, selected_lines)
            outfile.write(line)

    def get_line_to_write(self, index, selected_lines):
        """Determine which line to write for a given index.

        Args:
            index (int): Line index
            selected_lines (dict): Dictionary of user selections

        Returns:
            str: The line to write
        """
        # Get the line based on selection or default
        if index in selected_lines:
            line = self.lines1[index] if selected_lines[index] == 1 else self.lines2[index]
        else:
            line = self.lines1[index] if index < len(self.lines1) else self.lines2[index]

        # Ensure line ends with newline but doesn't have extra ones
        line = line.rstrip('\n') + '\n'
        
        return line

    def filter_lines(self, lines):
        """Filter lines to keep only those containing INSERT statements.

        Args:
            lines (list): List of lines to filter

        Returns:
            list: Filtered lines containing INSERT statements
        """
        return [line for line in lines if INSERT_KEYWORD in line]

    def strip_common_prefix(self, line):
        """Remove the common SQL prefix from a line if present.

        Args:
            line (str): Line to process

        Returns:
            str: Line with common prefix removed
        """
        if line.startswith(COMMON_PREFIX):
            return line[len(COMMON_PREFIX):]
        return line

    def extract_verse_info(self, line):
        """Extract book code, chapter, verse number, and text from a SQL line.
        
        Args:
            line (str): SQL line to parse
            
        Returns:
            tuple: (book_code, chapter, verse_num, verse_text)
        """
        match = re.search(VERSE_REGEX, line)
        if match:
            book_code, chapter, verse_num, verse_text = match.groups()
            return book_code, chapter, verse_num, verse_text
        return "", "", "", line

    def navigate_to_verse(self):
        """Navigate to the selected book, chapter, and verse."""
        try:
            target_book = self.book_combo.get()
            target_chapter = self.chapter_combo.get()
            target_verse = self.verse_combo.get()
            
            if not all([target_book, target_chapter, target_verse]):
                tk.messagebox.showwarning("Warning", "Please select book, chapter and verse")
                return
            
            # Search through lines to find matching verse
            for i, line in enumerate(self.lines1):
                book, chapter, verse, _ = self.extract_verse_info(line)
                if (book == target_book and 
                    str(chapter) == str(target_chapter) and 
                    str(verse) == str(target_verse)):
                    self.current_line = i
                    self.show_line()
                    return
            
            tk.messagebox.showinfo("Not Found", 
                f"Verse {target_book} {target_chapter}:{target_verse} not found")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Navigation failed: {e}")

    def update_navigation_options(self):
        """Update the navigation comboboxes with available options."""
        books = self.get_available_books()
        chapters = self.get_available_chapters(self.book_combo.get())
        verses = self.get_available_verses(self.book_combo.get(), self.chapter_combo.get())
        
        self.update_combo_values(self.book_combo, books)
        self.update_combo_values(self.chapter_combo, chapters, convert_to_int=True)
        self.update_combo_values(self.verse_combo, verses, convert_to_int=True)

    def get_available_books(self):
        """Get set of available book codes from file1.
        
        Returns:
            set: Available book codes
        """
        return {book for line in self.lines1 
                if (book := self.extract_verse_info(line)[0])}

    def get_available_chapters(self, current_book):
        """Get set of available chapters for the current book.
        
        Args:
            current_book (str): Currently selected book code
            
        Returns:
            set: Available chapter numbers
        """
        return {chapter for line in self.lines1 
                if (book := self.extract_verse_info(line)[0]) == current_book
                and (chapter := self.extract_verse_info(line)[1])}

    def get_available_verses(self, current_book, current_chapter):
        """Get set of available verses for the current book and chapter.
        
        Args:
            current_book (str): Currently selected book code
            current_chapter (str): Currently selected chapter number
            
        Returns:
            set: Available verse numbers
        """
        return {verse for line in self.lines1 
                if (book := self.extract_verse_info(line)[0]) == current_book
                and (chapter := self.extract_verse_info(line)[1]) == current_chapter
                and (verse := self.extract_verse_info(line)[2])}

    def update_combo_values(self, combo, values, convert_to_int=False):
        """Update a combobox with new values and maintain selection if possible.
        
        Args:
            combo (ttk.Combobox): Combobox to update
            values (set): New values to display
            convert_to_int (bool): Whether to sort numerically
        """
        if not values:
            combo.set('')
            combo['values'] = []
            return

        sorted_values = sorted(values, key=int) if convert_to_int else sorted(values)
        combo['values'] = sorted_values
        
        if not combo.get():
            combo.set(sorted_values[0])

if __name__ == "__main__":
    import os

    # Get the base directory (where the script is located)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Default file paths using os.path.join for proper path separators
    default_file1 = os.path.join(base_dir, "..", "bookish-lamp", "generatedSQL", "bibleVersesNS.sql")
    default_file2 = os.path.join(base_dir, "..", "bookish-lamp", "comparisons", "2024_WEB_Changes.sql")
    
    # Create the application with default files
    app = BibleHarmonyApp(default_file1, default_file2)
    
    # Try to load the files immediately
    try:
        # Load and process the files
        if app.read_files():
            app.filter_and_validate_lines()
            app.show_line()
    except Exception as e:
        print(f"Could not load default files: {e}")

    app.mainloop()
