import os
from bibleModule import myBookAbbrFromWEB, notApocrypha, lpadNum

t_path = 'eng-web_html'

def make_sql(t_book, t_chapter, t_verse):
    t_sql_start = "INSERT INTO `verses` (`bookCode`, `chapter`, `verseNumber`, `verseText`) VALUES ("
    t_sql_start += "'" + t_book + "'" + "," + t_chapter  + "," + lpadNum(t_verse) + "\n"
    return t_sql_start

def get_chapter(t_chapter):
    if '.' in t_chapter:
        t_chapter = t_chapter[:-1]
    i_chapter = int(t_chapter)
    return lpadNum(str(i_chapter))

def get_verse_number(t_line):
    verse_num_index = t_line.find('id="V') + 5
    verse_num_text = t_line[verse_num_index:verse_num_index + 3]
    verse_num_end = verse_num_text.find('"') 
    print(verse_num_text[:verse_num_end])
    return verse_num_text[:verse_num_end]

def main():
    print('get paragraphs from WEB HTML files')
    t_file = 'ParasFrom_WEB-HTML.txt'

    t_line = ''

    fw = open(t_path + '\\' + t_file, 'w', encoding="utf8")

    t_book = ''
    t_chapter = ''
    t_verse_text = ''
    t_verse_num = ''
    t_para = "<div class='p'>"

    for filename in os.listdir(t_path):
        if filename.endswith('.htm'):
            t_book = myBookAbbrFromWEB(filename[0:3])
            t_chapter = get_chapter(filename[3:6])

            print(t_book + ':' + '[' + t_chapter + ']')

            if notApocrypha(t_book):
                print('')
                print('processing ' + filename + ':')
                print('')
                fr = open(t_path + '\\' +filename, 'r', encoding="utf8")

                t_line = fr.readline()
                while t_line:
                    if t_para in t_line:
                        while t_para in t_line:
                            verse_index = t_line.find(t_para)
                            t_verse_text  = t_line[verse_index:verse_index + 77]
                            t_verse_num = get_verse_number(t_verse_text)
                            if t_verse_num > '0':
                                fw.write(make_sql(t_book, t_chapter, t_verse_num) + t_verse_text)
                            t_line  = t_line[verse_index + 1:]
                    t_line = fr.readline()                   
                fr.close()
    fw.close()

main()
