import os, string

def main():
    dir_comparisons = "comparisons"
    dir_mine = "generatedSQL"

    file_2024 = os.path.join(dir_comparisons, "USFM_2024-08-21_bible1NS.sql")
    file_mine = os.path.join(dir_mine, "bibleVersesNS.sql")
    output_file = os.path.join(dir_mine, "bibleVerses_2024_WEB_Puntuation.sql")

    print("--------------------------------------------------------------------")
    print(f"Comparing files:\n1: {file_mine}\n2: {file_2024}")
    print("--------------------------------------------------------------------")

    with open(file_2024, "r") as fr1, \
         open(file_mine, "r") as fr2, \
         open(output_file, "w") as fw:

        # Skip to first INSERT statement
        line_2024 = skip_to_insert(fr1)
        line_mine = skip_to_insert(fr2)

        book = line_2024[82:85]
        print(f"\n{book}")

        while line_2024 or line_mine:
            new_book = line_2024[82:85] if line_2024 else "END"
            if new_book != book:
                book = new_book
                print(f"\n{book}")

            if line_2024 == line_mine:
                print(".", end="")
                fw.write(line_mine[:98] + '\n')
            else:
                if change_is_punctuation(line_2024,line_mine):
                    fw.write(line_2024)
                    fw.write(line_mine)
                    print("P", end="")
                else:
                    fw.write(line_2024[:98] + '\n')
                    print("T", end="")

            line_2024 = fr1.readline() if line_2024 else ""
            line_mine = fr2.readline() if line_mine else ""

    print("\nComparison complete.")

def skip_to_insert(file):
    """Skips lines until it finds an 'INSERT INTO' statement."""
    for line in file:
        if line.startswith("INSERT INTO "):
            return line
    return ""

def get_my_line(fr3, target_line, current_line):
    """Finds the corresponding line in the user's file."""
    while not current_line.startswith(target_line[:98]):
        current_line = fr3.readline()

    return current_line

def change_is_punctuation(line_2024, line_mine):
    """if the ONLY change is punctuation, return the line, else just the first 98 chars"""
    is_punctuation = keep_checking = True
    i_2024 = i_mine = 99

    while keep_checking and i_2024 < len(line_2024) and i_mine < len(line_mine):
        char_2024 = line_2024[i_2024]
        char_mine = line_mine[i_mine]
        print_progress(char_2024, char_mine, i_2024, i_mine)
        if char_2024 == "'" or char_mine == "'": # last character so end
            keep_checking = False
        elif char_mine == char_2024: # same character so move on
            i_2024 = i_2024 + 1
            i_mine = i_mine + 1
        else:
            if char_2024 in string.punctuation or char_mine in string.punctuation: # punctuation difference
                if char_2024 in string.punctuation:
                    i_2024 = i_2024 + 1
                elif char_mine in string.punctuation:
                    i_mine = i_mine + 1
            else: # alphabetic difference
                is_punctuation = False
                keep_checking = False
                print_progress(char_2024, char_mine, i_2024, i_mine)

    return is_punctuation

def print_progress(char_2024, char_mine, i_2024, i_mine):
    # print (f"4:{i_2024},{char_2024};m{i_mine},{char_mine}") # this is for debugging
    print("", end="")

if __name__ == "__main__":
    main()
