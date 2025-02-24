import PySimpleGUI as sg

# List of books from the Bible
books = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
    "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon",
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
    "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians",
    "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians",
    "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
]

# Define the layout of the GUI
layout = [
    [sg.Text('Select a book from the Bible:')],
    [sg.Listbox(values=books, size=(30, 20), key='-BOOK-', enable_events=True)],
    [sg.Text('Enter Chapter:'), sg.InputText(key='-CHAPTER-', size=(5, 1))],
    [sg.Text('Enter Verse:'), sg.InputText(key='-VERSE-', size=(5, 1))],
    [sg.Button('OK'), sg.Button('Cancel')],
    [sg.Text('URL:'), sg.InputText(key='-URL-', size=(50, 1))]
]

# Create the window
window = sg.Window('Select Bible Book', layout)

# Event loop to process events and get the selected book, chapter, and verse
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        break
    if event == 'OK':
        selected_book = values['-BOOK-'][0] if values['-BOOK-'] else None
        chapter = values['-CHAPTER-']
        verse = values['-VERSE-']
        if selected_book and chapter and verse:
            url = f'https://www.biblegateway.com/verse/en/{selected_book}%20{chapter}%3A{verse}'
            window['-URL-'].update(url)
        else:
            sg.popup('Please select a book and enter both chapter and verse.')

# Close the window
window.close()