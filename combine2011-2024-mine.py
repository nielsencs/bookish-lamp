# This is based on my compare2filesNew.py
# I am comparing the latest WEB (actually 2024-08) with the earliest version I have (2011) on a verse by verse basis and creating a new file with:
# My text, unless the 2024 and 2011 texts differ, in which case the 2024 text
# This should eliminate the possibility of my unneccesarily comparing text I've already updated from the 2011 one.

import os

def main():
    t_path_1 = 'comparisons\\'
    t_path_2 = 'generatedSQL\\'

    t_file_1 =  t_path_1 + 'WEB(2011)bibleNS.sql'
    t_file_2 =  t_path_1 + 'USFM_2024-08-21_bible1NS.sql'
    t_file_3 =  t_path_2 + 'bibleVersesNS.sql'

    t_line_1 = ''
    t_line_2 = ''
    t_line_3 = ''

    t_book = ''

    # Print confirmation
    print('--------------------------------------------------------------------')
    print('Comparing files ', ' 1: ' + t_file_1, ' 2: ' +t_file_2, sep='\n')
    print('--------------------------------------------------------------------')

    fw = open('comparisons\\2024_WEB_Changes.sql', 'w', encoding="utf8")

    fr1 = open(t_file_1, 'r', encoding="utf8")
    t_line_1 = fr1.readline()
    while not t_line_1[:12] == 'INSERT INTO ':
        t_line_1 = fr1.readline()
    t_book = t_line_1[82:85]
    print('\n' + t_book)

    fr2 = open(t_file_2, 'r', encoding="utf8")
    t_line_2 = fr2.readline()
    while not t_line_2[:12] == 'INSERT INTO ':
        t_line_2 = fr1.readline()

    fr3 = open(t_file_3, 'r', encoding="utf8")
    while not t_line_3[:12] == 'INSERT INTO ':
        t_line_3 = fr1.readline()

    while t_line_1 or t_line_2:
        t_book_new = t_line_1[82:85]
        if t_book_new != t_book:
            t_book = t_book_new
            print('\n' + t_book)
        if t_line_1 == t_line_2:
            t_line_3 = get_my_line(fr3, t_line_1, t_line_3)
            print('.', end='')
            fw.write(t_line_3)
        else:
            print('D', end='')
            fw.write(t_line_2)

        t_line_1 = fr1.readline()
        t_line_2 = fr2.readline()

    fr1.close()
    fr2.close()
    fr3.close()
    fw.close()

def get_my_line(fr3, t_line_1, t_line_3):
    while t_line_3[:99] != t_line_1[:99]:
        t_line_3 = fr3.readline()
    return t_line_3

main()
