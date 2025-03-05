# Purpose: To check the AV (USFM_2006_KJV0.sql file) and output the occurences of ye, you, your, yours.
import os, re

def main():
    # Define the old English words to detect
    old_english_words = ["ye", "you", "your", "yours"]

    # Define a regular expression pattern to match the old English words
    pattern = re.compile(r'\b(?:' + '|'.join(old_english_words) + r')\b', re.IGNORECASE)

    t_dir = "generatedSQL"
    t_file_input = os.path.join(t_dir, "USFM_2006_KJV0.sql")
    t_file_output = os.path.join(t_dir, "AVYous.sql")

    print("--------------------------------------------------------------------")
    print(f"Processing {t_file_input}")
    print("--------------------------------------------------------------------")

    # with open(t_file_input, 'r', encoding='utf-8') as file:
    #     for line_number, line in enumerate(fr, start=1):
    #         matches = pattern.findall(line)
    #         if matches:
    #             print(f"Line {line_number}: {', '.join(matches)}")
    #         else:
    with open(t_file_input, "r") as fr, \
         open(t_file_output, "w") as fw:

        # Skip to first INSERT statement
        t_line_AV = skip_to_insert(fr)

        book = t_line_AV[82:85]
        print(f"\n{book}")

        while t_line_AV:
            new_book = t_line_AV[82:85] if t_line_AV else "END"
            if new_book != book:
                book = new_book
                print(f"\n{book}")

            matches = pattern.findall(t_line_AV)
            if matches:
                # print(f"Line {line_number}: {', '.join(matches)}")
                # fw.write(t_line_AV + f"{''.join(matches)}")
                fw.write(t_line_AV)
                print("Y", end="")
            else:
                # fw.write(t_line_AV[:98] + '\n')
                print(".", end="")

            t_line_AV = fr.readline() if t_line_AV else ""

    print("\nProcessing complete.")

def skip_to_insert(file):
    """Skips lines until it finds an 'INSERT INTO' statement."""
    for line in file:
        if line.startswith("INSERT INTO "):
            return line
    return ""

if __name__ == "__main__":
    main()
