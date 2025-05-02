# BibleHarmony

A Python/Tkinter application for comparing and editing Bible verses in SQL format. It provides side-by-side comparison of three files with color-coded difference highlighting and verse navigation.

## Key Features

### File Management
- Compare two Bible verse files, one of which has been created automatically from a master reference file
- Auto-load last used files from config
- Configurable default paths
- Preserves SQL formatting

### Navigation
- Book/Chapter/Verse dropdown navigation
- Previous/Next navigation for Books (Prev B/Next B)
- Previous/Next navigation for Chapters (Prev C/Next C)
- Previous/Next navigation for Verses (Prev/Next)
- "Hide Identical Lines" option to skip matching verses

### Text Display
- Color-coded difference highlighting:
  - Light green: Case differences
  - Bright yellow: Punctuation differences
  - Light pink: Other differences
- Editable master text field
- Auto-saving of master text changes

### Processing Options
- Strip Strong's numbers (`{H####}` and `{G####}`)
- Strip HTML formatting (`<p>`, `</br>`, etc.)
- Strip escaped quotes
- Word substitutions (configurable)

## Quick Start

1. Launch the application
2. Files will auto-load from default locations:
   ```
   generatedSQL/bibleVersesNS.sql
   comparisons/2024_WEB_Changes.sql
   database/bibleVerses.sql
   ```

3. Navigate using:
   - Dropdown menus for Book/Chapter/Verse
   - Navigation buttons for Previous/Next
   - Keyboard shortcuts:
     - Ctrl+Left: Previous verse
     - Ctrl+Right: Next verse
     - Ctrl+Up: Previous chapter
     - Ctrl+Down: Next chapter

4. Edit master text:
   - Changes auto-save when typing
   - Click "Save" to write to disk and update File 1

## File Format
Files should contain SQL INSERT statements in the format:
```sql
INSERT INTO `verses` (`bookCode`, `chapter`, `verseNumber`, `verseText`) 
VALUES ('GEN', 1, 1, 'verse text here');
```

## Configuration
Settings are stored in `config.json`:
- Default file paths
- Last used files
- Window size

## Status Information
The status bar shows:
- Current verse reference
- Current line number
- Total lines in each file
- Line count for master file (if loaded)