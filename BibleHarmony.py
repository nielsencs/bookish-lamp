"""
TODO List:
1. Incorporate stripStrongs_bibleVerses_GUI functionality: DONE!
    - make word swaps selectable

2. Add master file handling: DONE!

3. Improve GUI layout: DONE!

4. Improve Editing
    - ctrl-z to undo, ctrl-y to redo (it already has ctrl-a to select all, ctrl-c to copy, ctrl-v to paste) DONE!
    - automatic acceptance of file 2 punctuation or other differences possibly based on highlighting
    - improve the way the text is highlighted - overdone in verse NEH 5:15 - too long (actually fine!)

N. Future Enhancements:
    - Add configuration for default paths DONE!
    - Add configuration for default window size DONE!
    - Save/restore last used settings - especially current book, chapter and verse (see 2 above)
    - remove the actual file1 - it's just a processed master file - process at load time rather than save time DONE!
    - smart copying of text from comparison_file to master file - only copy the selected text, not the whole line
    - rename File 1 to processed Master File or something similar
    - rename File 2 to Comparison File or something similar
    - process Comparison file on loading

"""

PADDING = 10
TEXT_HEIGHT = 5
WINDOW_MIN_WIDTH = 770
WINDOW_MIN_HEIGHT = 660

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
import json
import os

HIGHLIGHT_COLORS = {
    "case": "#90EE90",         # Light green
    "punctuation": "#FFFF00",  # Bright yellow
    "other": "#FFB6C1",        # Light pink
}

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

    # My alternate codes!
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
    'NAM': 34,  # Nahum
    'JHO': 43,  # John
    'PHI': 50  # Philippians
}

CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from JSON file."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default config if file doesn't exist
        config = {
            "default_paths": {
                "comparison": os.path.join("comparisons", "2024_WEB_Changes.sql"),
                "master": os.path.join("database", "bibleVerses.sql")
            },
            "last_used": {
                "comparison": "",
                "master": ""
            },
            "window": {
                "width": WINDOW_MIN_WIDTH + 300,
                "height": WINDOW_MIN_HEIGHT
            }
        }
        save_config(config)
        return config

def save_config(config):
    """Save configuration to JSON file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

class BibleHarmonyApp(tk.Tk):
    """A tkinter application for comparing and editing Bible verse files."""

    def __init__(self, comparison_file, master_file):
        super().__init__()
        
        # Load configuration
        self.config = load_config()
        
        # Use last used paths if available, otherwise use defaults
        # self.file1 = self.config["last_used"]["file1"] or file1 or self.config["default_paths"]["file1"]
        self.comparison_file = self.config["last_used"]["comparison"] or comparison_file or self.config["default_paths"]["comparison"]
        self.master_file = self.config["last_used"]["master"] or master_file or self.config["default_paths"]["master"]
        
        # Set window size from config
        self.geometry(f"{self.config['window']['width']}x{self.config['window']['height']}")

        self.title("BibleHarmony")  # Set the window title
        self.current_line = 0
        self.total_lines = 0

        # Initialize the line lists
        self.processed_lines = []
        self.comparison_lines = []
        
        # Set a minimum size for the window
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Configure the grid to allow column expansion
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Navigation Frame
        nav_frame = tk.LabelFrame(self, text="Navigation")
        nav_frame.grid(row=0, column=0, columnspan=2, sticky="EW", padx=PADDING)

        # Book navigation
        book_frame = tk.Frame(nav_frame)
        book_frame.pack(side="left", padx=5)
        tk.Label(book_frame, text="Book:").pack(side="left")
        self.book_combo = ttk.Combobox(book_frame, width=5)
        self.book_combo.pack(side="left")
        self.prev_B_button = tk.Button(book_frame, text="Prev B", command=self.prev_book)
        self.prev_B_button.pack(side="left")
        self.next_B_button = tk.Button(book_frame, text="Next B", command=self.next_book)
        self.next_B_button.pack(side="left")

        # Chapter navigation
        chapter_frame = tk.Frame(nav_frame)
        chapter_frame.pack(side="left", padx=5)
        tk.Label(chapter_frame, text="Chapter:").pack(side="left")
        self.chapter_combo = ttk.Combobox(chapter_frame, width=3)
        self.chapter_combo.pack(side="left")
        self.prev_c_button = tk.Button(chapter_frame, text="Prev C", command=self.prev_chapter)
        self.prev_c_button.pack(side="left")
        self.next_button = tk.Button(chapter_frame, text="Next C", command=self.next_chapter)
        self.next_button.pack(side="left")

        # Verse navigation
        verse_frame = tk.Frame(nav_frame)
        verse_frame.pack(side="left", padx=5)
        tk.Label(verse_frame, text="Verse:").pack(side="left")
        self.verse_combo = ttk.Combobox(verse_frame, width=3)
        self.verse_combo.pack(side="left")
        self.prev_button = tk.Button(verse_frame, text="Prev", command=self.prev_line)
        self.prev_button.pack(side="left")
        self.next_button = tk.Button(verse_frame, text="Next", command=self.next_line)
        self.next_button.pack(side="left")

        # 'Hide Identical Lines' option
        self.hide_identical_var = tk.BooleanVar(value=False)
        tk.Checkbutton(nav_frame, text="Hide Identical Lines", 
                       variable=self.hide_identical_var,
                       command=self.show_line).pack(side="left", padx=5)

        # File 1 Frame
        file1_frame = tk.LabelFrame(self, text="File 1")
        file1_frame.grid(row=1, column=0, columnspan=2, sticky="NSEW", padx=PADDING, pady=5)
        
        file1_header = tk.Frame(file1_frame)
        file1_header.pack(fill="x", padx=5, pady=2)
        self.file1_name_label = tk.Label(file1_header, text=NO_FILE_MSG, anchor="w")
        self.file1_name_label.pack(side="left", fill="x", expand=True)
        
        self.file1_text = tk.Text(file1_frame, height=TEXT_HEIGHT, wrap="word", state="disabled")
        self.file1_text.pack(fill="both", expand=True, padx=5, pady=2)

        # File 2 Frame
        file2_frame = tk.LabelFrame(self, text="File 2")
        file2_frame.grid(row=2, column=0, columnspan=2, sticky="NSEW", padx=PADDING, pady=5)
        
        file2_header = tk.Frame(file2_frame)
        file2_header.pack(fill="x", padx=5, pady=2)
        self.file2_name_label = tk.Label(file2_header, text=NO_FILE_MSG, anchor="w")
        self.file2_name_label.pack(side="left", fill="x", expand=True)
        self.file2_button = tk.Button(file2_header, text="Select File", command=self.select_file)
        self.file2_button.pack(side="right")
        
        self.file2_text = tk.Text(file2_frame, height=TEXT_HEIGHT, wrap="word", state="disabled")
        self.file2_text.pack(fill="both", expand=True, padx=5, pady=2)

        # Add auto-accept buttons frame between File 2 and Master
        auto_accept_frame = tk.LabelFrame(self, text="Auto Accept")
        auto_accept_frame.grid(row=3, column=0, columnspan=2, sticky="EW", padx=PADDING, pady=5)

        # Add buttons for each difference type
        tk.Button(auto_accept_frame, text="Accept Case", 
                  command=lambda: self.accept_differences("case"),
                  bg=HIGHLIGHT_COLORS["case"]).pack(side="left", padx=5)
        tk.Button(auto_accept_frame, text="Accept Punctuation", 
                  command=lambda: self.accept_differences("punctuation"),
                  bg=HIGHLIGHT_COLORS["punctuation"]).pack(side="left", padx=5)
        tk.Button(auto_accept_frame, text="Accept Other", 
                  command=lambda: self.accept_differences("other"),
                  bg=HIGHLIGHT_COLORS["other"]).pack(side="left", padx=5)

        # Master File Frame (now at row 4)
        master_frame = tk.LabelFrame(self, text="Master File")
        master_frame.grid(row=4, column=0, columnspan=2, sticky="NSEW", padx=PADDING, pady=5)

        master_header = tk.Frame(master_frame)
        master_header.pack(fill="x", padx=5, pady=2)
        self.master_name_label = tk.Label(master_header, text=NO_FILE_MSG, anchor="w")
        self.master_name_label.pack(side="left", fill="x", expand=True)

        self.master_text = tk.Text(master_frame, height=TEXT_HEIGHT, wrap="word", undo=True, maxundo=-1)
        self.master_text.pack(fill="both", expand=True, padx=5, pady=2)
        self.master_text.bind('<<Modified>>', self.store_master)

        # Controls Frame
        controls_frame = tk.LabelFrame(self, text="Controls")
        controls_frame.grid(row=5, column=0, columnspan=2, sticky="EW", padx=PADDING, pady=5)
        
        self.save_button = tk.Button(controls_frame, text="Save", command=self.save_master_file)
        self.save_button.pack(side="top", pady=2)
        
        buttons_frame = tk.Frame(controls_frame)
        buttons_frame.pack(fill="x", padx=5, pady=2)

        # Add save buttons
        save_frame = tk.Frame(controls_frame)
        save_frame.pack(fill="x", padx=5, pady=2)
        
        # Add processing options frame
        options_frame = tk.LabelFrame(controls_frame, text="Processing Options")
        options_frame.pack(fill="x", padx=5, pady=2)
        
        # Initialize checkbox variables
        self.strip_strongs_var = tk.BooleanVar(value=True)     # Strip Strong's numbers
        self.strip_formatting_var = tk.BooleanVar(value=True)  # Strip HTML formatting (<p>, <br>, etc.)
        self.strip_quotes_var = tk.BooleanVar(value=True)      # Strip quotes from the verse text
        self.swap_words_var = tk.BooleanVar(value=True)        # Swap words in the verse text (eg "group" for "company")
        
        # Add checkboxes
        tk.Checkbutton(options_frame, text="Strip Strong's Numbers", 
                       variable=self.strip_strongs_var).pack(side="left", padx=5)
        tk.Checkbutton(options_frame, text="Strip Formatting", 
                       variable=self.strip_formatting_var).pack(side="left", padx=5)
        tk.Checkbutton(options_frame, text="Strip Quotes", 
                       variable=self.strip_quotes_var).pack(side="left", padx=5)
        tk.Checkbutton(options_frame, text="Swap Words", 
                       variable=self.swap_words_var).pack(side="left", padx=5)

        # Status Bar
        status_frame = tk.LabelFrame(self, text="Status")
        status_frame.grid(row=7, column=0, columnspan=2, sticky="EW", padx=PADDING, pady=5)
        self.status_bar = tk.Label(status_frame, text="Line 1 of 100", anchor="w")
        self.status_bar.pack(fill="x", padx=5, pady=2)

        # Show the first line
        self.show_line()

        self.bind("<Control-s>", lambda event: self.save_master_file())
        self.bind("<Up>", lambda event: self.prev_line())
        self.bind("<Down>", lambda event: self.next_line())
        self.bind("<Control-Up>", lambda event: self.prev_chapter())
        self.bind("<Control-Down>", lambda event: self.next_chapter())

        # Automate lookup from book, chapter & verse combos
        self.book_combo.bind('<<ComboboxSelected>>', lambda e: self.navigate_to_verse())
        self.chapter_combo.bind('<<ComboboxSelected>>', lambda e: self.navigate_to_verse())
        self.verse_combo.bind('<<ComboboxSelected>>', lambda e: self.navigate_to_verse())

        # Add current location tracking
        self.current_book = "NEH"
        self.current_chapter = "5"
        self.current_verse = "18"

        # Add verse index dictionaries
        self.verse_index1 = {}  # For processed master file
        self.verse_index2 = {}  # For comparison_file
        self.verse_index_master = {}  # For master file

    def select_file(self):
        """Open a file dialog to select a file and update the display."""
        file_path = filedialog.askopenfilename(
            title="Select Comparison File",
            initialdir=os.path.dirname(self.config["last_used"]["comparison_file"] or 
                                     self.config["default_paths"]["comparison_file"])
        )
        if file_path:
            try:
                with open(file_path, "r", encoding=ENCODING, errors=ERRORS_POLICY):
                    self.comparison_file = file_path
                    self.file2_name_label.config(text=file_path)
                    
                    # Update last used paths in config
                    self.config["last_used"]["comparison_file"] = file_path
                    save_config(self.config)
                    
                    self.read_files()
                    self.filter_and_validate_lines()
                    self.current_line = 0
                    self.show_line()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to open comparison file: {e}")

    def select_master_file(self):
        """Open a file dialog to select the master file."""
        file_path = filedialog.askopenfilename(
            title="Select Master File",
            initialdir=os.path.dirname(self.config["last_used"]["master"] or 
                                 self.config["default_paths"]["master"])
        )
        if file_path:
            try:
                with open(file_path, "r", encoding=ENCODING, errors=ERRORS_POLICY):
                    self.master_file = file_path
                    self.master_name_label.config(text=file_path)
                    self.lines_master = self.read_and_filter_lines(file_path)
                    self.filter_and_validate_lines()
                    self.current_line = 0
                    self.show_line()
                
                # Update last used paths in config
                self.config["last_used"]["master"] = file_path
                save_config(self.config)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to open Master File: {e}")

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
        """Display the current line from all files and highlight differences."""
        try:
            # Check if we have any lines to display
            if not self.processed_lines:
                self.update_text_field(self.file1_text, "No verses loaded in File 1")
                self.update_text_field(self.file2_text, "No verses loaded in File 2")
                self.update_text_field(self.master_text, "No verses loaded in Master")
                self.master_text.edit_reset()  # Reset the undo stack
                return

            # Get the current lines
            text1, text2, _, _ = self.get_current_lines()

            # Update text fields
            self.update_text_field(self.file1_text, text1)
            self.update_text_field(self.file2_text, text2)

            # Find the matching master line
            master_line = None
            if hasattr(self, 'lines_master'):
                for line in self.lines_master:
                    book, chapter, verse, _ = self.extract_verse_info(line)
                    if (book == self.current_book and 
                        str(chapter) == str(self.current_chapter) and 
                        str(verse) == str(self.current_verse)):
                        master_line = line
                        break

            self.update_text_field(self.master_text, master_line if master_line else "No master verse found")
            self.master_text.edit_reset()  # Reset the undo stack
            
            # Highlight differences between text1 and text2
            if text1 and text2 and text1 != "No matching verse in File 1." and text2 != "No matching verse in File 2.":
                self.highlight_differences(text1, text2)

            # Update navigation display
            self.update_verse_display(self.current_book, self.current_chapter, self.current_verse)
            self.update_status()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to process files: {e}")

    def get_current_lines(self):
        """Get lines using direct index lookup."""
        key = (self.current_book, str(self.current_chapter), str(self.current_verse))
        
        # Direct index lookups instead of searching
        index1 = self.verse_index1.get(key)
        index2 = self.verse_index2.get(key)
        
        line1 = self.processed_lines[index1] if index1 is not None else None
        line2 = self.comparison_lines[index2] if index2 is not None else None
        
        # Extract verse info
        if line1:
            _, _, _, text1 = self.extract_verse_info(line1)
        else:
            text1 = "No matching verse in File 1."
            
        if line2:
            _, _, _, text2 = self.extract_verse_info(line2)
        else:
            text2 = "No matching verse in File 2."
            
        return text1, text2, line1, line2  # Return both text and full lines

    def process_master(self):
        """Process the master file to create processed_lines in memory."""
        self.processed_lines = []
        for line in self.lines_master:
            book, chapter, verse, text = self.extract_verse_info(line)
            
            # Apply processing in correct order
            if self.swap_words_var.get():
                text = self.swap_words(text)
            if self.strip_formatting_var.get():
                text = self.strip_formatting(text)
            if self.strip_quotes_var.get():
                text = self.strip_quotes(text)
            if self.strip_strongs_var.get():
                text = self.strip_strongs(text)
                
            # Create processed line
            processed_line = f"{COMMON_PREFIX}'{book}', {chapter}, {verse}, '{text}'{COMMON_SUFFIX}\n"
            self.processed_lines.append(processed_line)

    def read_files(self):
        """Read files and build verse indices."""
        try:
            # Update labels
            self.file2_name_label.config(text=self.comparison_file or NO_FILE_MSG)
            self.master_name_label.config(text=self.master_file or NO_FILE_MSG)
            self.file1_name_label.config(text="Processed Master File")  # New label

            if not self.comparison_file or not self.master_file:
                tk.messagebox.showerror("Error", "Both comparison and master files must be selected.")
                return False

            # Read comparison and master files
            with open(self.comparison_file, "r", encoding=ENCODING, errors=ERRORS_POLICY) as f2:
                self.comparison_lines = [line for line in f2 if INSERT_KEYWORD in line]
            with open(self.master_file, "r", encoding=ENCODING, errors=ERRORS_POLICY) as fmaster:
                self.lines_master = [line for line in fmaster if INSERT_KEYWORD in line]

            # Process master file to create processed_lines in memory
            self.process_master()
                    
            return True
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to read files: {e}")
            return False

    def filter_and_validate_lines(self):
        """Filter lines for SQL statements and ensure verses are aligned between files."""
        # First filter for SQL statements
        self.processed_lines = self.filter_lines(self.processed_lines)
        self.comparison_lines = self.filter_lines(self.comparison_lines)
        if hasattr(self, 'lines_master'):  # Leave master file as-is
            self.lines_master = self.filter_lines(self.lines_master)

        # Create dictionaries to map (book, chapter, verse) to line content
        processed_verses = {}
        comparison_verses = {}
        
        # Process file 1
        for line in self.processed_lines:
            book, chapter, verse, _ = self.extract_verse_info(line)
            if book and chapter and verse:
                key = (book, str(chapter), str(verse))
                processed_verses[key] = line
                
        # Process file 2
        for line in self.comparison_lines:
            book, chapter, verse, _ = self.extract_verse_info(line)
            if book and chapter and verse:
                key = (book, str(chapter), str(verse))
                comparison_verses[key] = line

        # Get all verse references in Bible order
        def verse_key(verse_tuple):
            book, chapter, verse = verse_tuple
            return (BIBLE_BOOKS_ORDER.get(book, 999), int(chapter), int(verse))

        all_verses = sorted(set(processed_verses.keys()) | set(comparison_verses.keys()), key=verse_key)
        
        # Rebuild comparison files with empty placeholders for missing verses
        self.processed_lines = []
        self.comparison_lines = []
        self.verse_index1 = {}  # Clear and rebuild indices
        self.verse_index2 = {}
        empty_line = f"{COMMON_PREFIX}'',0,0,''{COMMON_SUFFIX}\n"
        
        for i, verse_key in enumerate(all_verses):
            line1 = processed_verses.get(verse_key, empty_line)
            line2 = comparison_verses.get(verse_key, empty_line)
            self.processed_lines.append(line1)
            self.comparison_lines.append(line2)
            self.verse_index1[verse_key] = i  # Update indices
            self.verse_index2[verse_key] = i

        self.total_lines = len(all_verses)
        self.current_line = max(0, min(self.current_line, self.total_lines - 1))

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

    def highlight_differences(self, text1, text2):
        """Highlight differences between two texts using different colors.
        
        Args:
            text1 (str): Text from first file
            text2 (str): Text from second file
        """
        # Clear existing highlights
        for tag in HIGHLIGHT_COLORS.keys():
            self.file1_text.tag_remove(tag, "1.0", tk.END)
            self.file2_text.tag_remove(tag, "1.0", tk.END)

        # Configure highlight tags
        for tag, color in HIGHLIGHT_COLORS.items():
            self.file1_text.tag_configure(tag, background=color)
            self.file2_text.tag_configure(tag, background=color)

        # Compare texts using SequenceMatcher
        matcher = difflib.SequenceMatcher(None, text1, text2)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag in ("replace", "insert", "delete"):
                # Get the differing segments
                seg1 = text1[i1:i2]
                seg2 = text2[j1:j2]
                
                # Skip if segments are identical
                if seg1 == seg2:
                    continue
                    
                # Determine type of difference
                if seg1.lower() == seg2.lower():
                    highlight_type = "case"
                elif seg1.translate(str.maketrans("", "", ".,!?:;")) == seg2.translate(str.maketrans("", "", ".,!?:;")):
                    highlight_type = "punctuation"
                else:
                    highlight_type = "other"
                
                # Apply highlights
                self.file1_text.tag_add(highlight_type, f"1.{i1}", f"1.{i2}")
                self.file2_text.tag_add(highlight_type, f"1.{j1}", f"1.{j2}")

    def update_text_field(self, text_widget, content):
        """Update a text widget with new content.

        Args:
            text_widget (tk.Text): Text widget to update
            content (str): New content to display
        """
        text_widget.config(state="normal")  # Make widget editable
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, content)
        
        # Only disable if it's an error or empty message
        if content in ["No verses loaded", "Error displaying verse", "No master verse found"]:
            text_widget.config(state="disabled")

    def update_status(self):
        """Update the status bar with current line numbers and file statistics."""
        current_book = self.book_combo.get() or "?"
        current_chapter = self.chapter_combo.get() or "?"
        current_verse = self.verse_combo.get() or "?"
        
        master_status = ""
        if hasattr(self, 'lines_master'):
            master_status = f" | Master: {len(self.lines_master)} lines"
            
        self.status_bar.config(
            text=f"{current_book} {current_chapter}:{current_verse} | "
                 f"Line {self.current_line + 1} of {self.total_lines} | "
                 f"File 1: {len(self.processed_lines)} lines, File 2: {len(self.comparison_lines)} lines"
                 f"{master_status}"
        )


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
            book, chapter, verse, _ = self.extract_verse_info(self.processed_lines[self.current_line])
            self.current_book = book
            self.current_chapter = chapter
            self.current_verse = verse
            
            # Skip identical lines if option is enabled
            if self.hide_identical_var.get():
                while self.current_line > 0 and self.are_lines_identical(self.current_line):
                    self.current_line -= 1
                    book, chapter, verse, _ = self.extract_verse_info(self.processed_lines[self.current_line])
                    self.current_book = book
                    self.current_chapter = chapter
                    self.current_verse = verse
                    
            self.show_line()

    def next_line(self):
        """Move to the next line if available."""
        if self.current_line < self.total_lines - 1:
            self.current_line += 1
            book, chapter, verse, _ = self.extract_verse_info(self.processed_lines[self.current_line])
            self.current_book = book
            self.current_chapter = chapter
            self.current_verse = verse
            
            # Skip identical lines if option is enabled
            if self.hide_identical_var.get():
                while (self.current_line < self.total_lines - 1 and 
                       self.are_lines_identical(self.current_line)):
                    self.current_line += 1
                    book, chapter, verse, _ = self.extract_verse_info(self.processed_lines[self.current_line])
                    self.current_book = book
                    self.current_chapter = chapter
                    self.current_verse = verse
                    
            self.show_line()

    def are_lines_identical(self, line_index):
        """Check if lines at the given index are identical.
        
        Args:
            line_index (int): Index of lines to compare
            
        Returns:
            bool: True if lines are identical, False otherwise
        """
        try:
            _, _, _, text1 = self.extract_verse_info(self.processed_lines[line_index])
            _, _, _, text2 = self.extract_verse_info(self.comparison_lines[line_index])
            return text1.strip() == text2.strip()
        except:
            return False

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
            new_book = self.book_combo.get()
            if new_book != self.current_book:
                self.current_book = new_book
                self.current_chapter=1
                self.current_verse=1
                self.update_navigation_options()
            else:
                self.current_chapter = self.chapter_combo.get()
                self.current_verse = self.verse_combo.get()

            if not all([self.current_book, self.current_chapter, self.current_verse]):
                tk.messagebox.showwarning("Warning", "Please select book, chapter, and verse")
                return

            # Use the verse index for direct lookup
            key = (self.current_book, str(self.current_chapter), str(self.current_verse))
            index = self.verse_index1.get(key)
            
            if index is not None:
                self.current_line = index
                self.show_line()
                return

            tk.messagebox.showinfo("Not Found", 
                f"Verse {self.current_book} {self.current_chapter}:{self.current_verse} not found")
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
        """Get set of available book codes from master file.
        
        Returns:
            set: Available book codes
        """
        return {book for line in self.lines_master 
                if (book := self.extract_verse_info(line)[0])}

    def get_available_chapters(self, current_book):
        """Get set of available chapters for the current book.
        
        Args:
            current_book (str): Currently selected book code
            
        Returns:
            set: Available chapter numbers
        """
        return {chapter for line in self.processed_lines 
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
        return {verse for line in self.processed_lines 
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

    def strip_strongs(self, text):
        """Strip Strong's numbers from text.
        
        Args:
            text (str): Text containing Strong's numbers
            
        Returns:
            str: Text with Strong's numbers removed
        """
        # Strip {H####} and {G####} patterns
        text = re.sub(r'\{[HG]\d+\}', '', text)
        return text

    def strip_formatting(self, text):
        """Strip formatting tags from text.
        
        Args:
            text (str): Text containing formatting tags
            
        Returns:
            str: Clean text
        """
        # Strip <p>, </p>, <br>, [, ] tags
        text = text.replace('<p>', '').replace('</p>', '')
        text = text.replace('<br>', '')
        text = text.replace('[', '').replace(']', '')
        text.replace('\\add', '').replace('\\add*', '')
        return text

    def strip_quotes(self, text):
        """Strip quotes from text.
        
        Args:
            text (str): Text escaped quotes ("\"" and "\'")
            
        Returns:
            str: Clean text
        """
        # Strip ("\"" and "\'") quotes
        text = text.replace('\\\"', '').replace('\\\'', '')
        return text

    def swap_words(self, text):
        """Apply word substitutions.
        
        Args:
            text (str): Original text
            
        Returns:
            str: Text with words swapped
        """
        replacements = {
            'Don\\\'t': 'You shall not',
            'mustn\\\'t': 'shall not',
            'LordOfMine{H0136}': 'Lord{H0136}',
            'temporary-shelters': 'temporary shelters',
            'wide-place': 'wide place',
            'enter': 'come into',
            'pursue': 'chase',
            'group': 'company',
            'murmur': 'complain',
            'testimony': 'covenant', 
            'winepress': 'wine press',
            'throw': 'cast',
            #Add more word pairs here
        }

                # Apply all replacements
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def write_sql_header(self, outfile):
        """Write the SQL header for table creation.
        
        Args:
            outfile: File object to write to
        """
        outfile.write("DROP TABLE IF EXISTS `verses`;\n")
        outfile.write("CREATE TABLE `verses` (\n")
        outfile.write("  `verseID` int(11) NOT NULL AUTO_INCREMENT,\n")
        outfile.write("  `bookCode` varchar(3) NOT NULL,\n")
        outfile.write("  `chapter` smallint(4) NOT NULL,\n")
        outfile.write("  `verseNumber` smallint(4) NOT NULL,\n")
        outfile.write("  `verseText` text NOT NULL,\n")
        outfile.write("  PRIMARY KEY (`verseID`),\n")
        outfile.write("  UNIQUE KEY `book-chapter-verse` (`bookCode`,`chapter`,`verseNumber`)\n")
        outfile.write(") ENGINE=MyISAM DEFAULT CHARSET=latin1;\n\n")

    def save_master_file(self):
        """Save the master file and reprocess in-memory version."""
        if not hasattr(self, 'lines_master'):
            tk.messagebox.showerror("Error", "No master file loaded")
            return
        
        try:
            # Save unprocessed master file
            with open(default_master_file, "w", encoding=ENCODING) as outfile:
                self.write_sql_header(outfile)
                for line in self.lines_master:
                    outfile.write(line)
                outfile.write("\nCOMMIT;\n")
                
            # Reprocess master file in memory
            self.process_master()
            self.filter_and_validate_lines()
            
            # Go to the correct verse
            self.navigate_to_verse()
                
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save files: {e}")

    def store_master(self, event=None):
        """Store changes made to master text widget."""
        try:
            # Update matching master line
            for i, line in enumerate(self.lines_master):
                book, chapter, verse, _ = self.extract_verse_info(line)
                if (book == self.current_book and 
                    str(chapter) == str(self.current_chapter) and 
                    str(verse) == str(self.current_verse)):
                    self.lines_master[i] = self.master_text.get("1.0", "end-1c")  # Get the full SQL line
                    self.master_text.edit_modified(False)  # Reset modified flag
                    return

            tk.messagebox.showerror("Error", "Could not find matching verse in master file")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save changes: {e}")

    def accept_differences(self, diff_type):
        """Accept differences of specified type from File 2."""
        try:
            # Get current master text and extract just the verse text
            master_line = self.master_text.get("1.0", "end-1c")
            _, _, _, master_verse_text = self.extract_verse_info(master_line)
            
            # Get ranges for the specified difference type
            ranges = self.file2_text.tag_ranges(diff_type)
            
            # Process ranges in pairs (start, end) from last to first
            for i in range(len(ranges)-2, -1, -2):
                start = ranges[i]
                end = ranges[i+1]
                
                # Get the text from File 2 for this difference
                diff_text = self.file2_text.get(start, end)
                
                # Convert tkinter indices to row/column
                start_row, start_col = map(int, str(start).split('.'))
                end_row, end_col = map(int, str(end).split('.'))
                
                # Apply the change to just the verse text
                master_verse_text = master_verse_text[:start_col] + diff_text + master_verse_text[end_col:]
            
            # Reconstruct the full SQL line with the modified verse text
            new_master_line = f"{COMMON_PREFIX}'{self.current_book}', {self.current_chapter}, {self.current_verse}, '{master_verse_text}'{COMMON_SUFFIX}"
            
            # Update master text with modified line
            self.master_text.delete("1.0", tk.END)
            self.master_text.insert("1.0", new_master_line)
            
            # Save changes
            self.store_master()
            
            # Show updated verse
            self.show_line()
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to accept differences: {e}")


if __name__ == "__main__":
    import os

    # Get the base directory (where the script is located)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Default file paths
    default_comparison_file = os.path.join("comparisons", "2024_WEB_Changes.sql")
    default_master_file = os.path.join("database", "bibleVerses.sql")
    
    # Create the application with default files
    app = BibleHarmonyApp(default_comparison_file, default_master_file)
    
    # Try to load the files immediately
    try:
        # Load and process the files
        if app.read_files():
            app.filter_and_validate_lines()
            app.show_line()
    except Exception as e:
        print(f"Could not load default files: {e}")

    app.mainloop()
