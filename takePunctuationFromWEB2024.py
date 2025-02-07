import os

def main():
    dir_comparisons = "comparisons"
    dir_mine = "generatedSQL"

    file_2011 = os.path.join(dir_comparisons, "WEB(2011)bibleNS.sql")
    file_2024 = os.path.join(dir_comparisons, "USFM_2024-08-21_bible1NS.sql")
    file_mine = os.path.join(dir_mine, "bibleVersesNS.sql")
    output_file = os.path.join(dir_mine, "bibleVerses_2024_WEB_Puntuation.sql")

    print("--------------------------------------------------------------------")
    print(f"Comparing files:\n1: {file_2011}\n2: {file_2024}")
    print("--------------------------------------------------------------------")

    with open(file_2011, "r") as fr1, \
         open(file_2024, "r") as fr2, \
         open(file_mine, "r") as fr3, \
         open(output_file, "w") as fw:

        # Skip to first INSERT statement
        line_2011 = skip_to_insert(fr1)
        line_2024 = skip_to_insert(fr2)
        line_mine = skip_to_insert(fr3)

        book = line_2011[82:85]
        print(f"\n{book}")

        while line_2011 or line_2024:
            new_book = line_2011[82:85] if line_2011 else "END"
            if new_book != book:
                book = new_book
                print(f"\n{book}")

            if line_2011 == line_2024:
                line_mine = get_my_line(fr3, line_2011, line_mine)
                print(".", end="")
                fw.write(line_mine)
            else:
                print("D", end="")
                fw.write(line_2024)

            line_2011 = fr1.readline() if line_2011 else ""
            line_2024 = fr2.readline() if line_2024 else ""

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

if __name__ == "__main__":
    main()
