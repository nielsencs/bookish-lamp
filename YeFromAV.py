import re

# Define the old English words to detect
old_english_words = ["ye", "you", "your", "yours"]

# Define a regular expression pattern to match the old English words
pattern = re.compile(r'\b(?:' + '|'.join(old_english_words) + r')\b', re.IGNORECASE)

# Path to the SQL file
file_path = 'D:/Python/bookish-lamp/generatedSQL/USFM_2006_KJV0.sql'

# Function to read the file and detect old English words
def detect_old_english_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            matches = pattern.findall(line)
            if matches:
                print(f"Line {line_number}: {', '.join(matches)}")

# Run the function
detect_old_english_words(file_path)