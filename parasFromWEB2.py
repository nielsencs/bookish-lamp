import os
from pathlib import Path
from bibleModule import myBookAbbrFromWEB, notApocrypha, lpadNum

input_path = Path('eng-web_html')

def make_sql(book_code, chapter, verse_number, verse_text):
    sql_start = (
        "INSERT INTO `verses` (`bookCode`, `chapter`, `verseNumber`, `verseText`) "
        f"VALUES ('{book_code}', {chapter}, {verse_number}, '{verse_text}');\n"
    )
    return sql_start

def get_chapter(chapter_str):
    chapter_str = chapter_str.rstrip('.')
    chapter_num = int(chapter_str)
    return lpadNum(str(chapter_num))

def get_verse_number(line):
    verse_num_index = line.find('id="V') + 5
    verse_num_text = line[verse_num_index:verse_num_index + 3]
    verse_num_end = verse_num_text.find('"') 
    return verse_num_text[:verse_num_end]

def process_file(file_path, output_file):
    book_code = myBookAbbrFromWEB(file_path.stem[:3])
    chapter = get_chapter(file_path.stem[3:6])

    if not notApocrypha(book_code):
        return

    print(f'Processing {file_path.name} ({book_code}:{chapter})')

    para_marker = "<div class='p'>"
    with file_path.open('r', encoding='utf8') as fr:
        for line in fr:
            while para_marker in line:
                verse_index = line.find(para_marker)
                verse_text = line[verse_index:verse_index + 77]
                verse_num = get_verse_number(verse_text)
                if verse_num > '0':
                    output_file.write(make_sql(book_code, chapter, lpadNum(verse_num), verse_text))
                line = line[verse_index + 1:]

def main():
    print('Extracting paragraphs from WEB HTML files')
    output_file_path = input_path / 'ParasFrom_WEB-HTML.txt'

    with output_file_path.open('w', encoding='utf8') as fw:
        for file_path in input_path.glob('*.htm'):
            process_file(file_path, fw)

if __name__ == '__main__':
    main()
