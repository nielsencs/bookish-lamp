import os
from bibleModule import *

import tkinter as tk
from tkinter import filedialog

oRoot = tk.Tk()
oRoot.withdraw()

#globals
tPath1 = 'database\\'
tPath2 = 'eng-web_usfm_2020-06-01\\'

tFile1 = ''
tFile2 = ''

tLine1 = ''
tLine2 = ''

tBook = ''

def main():
    # Ask the user to enter the names of files to compare
    tFile1 = filedialog.askopenfilename(initialdir = tPath1,
                                       title = 'Select file',
                                       filetypes = (('SeQueL files','*.sql'),('TeXT files','*.txt'),('all files','*.*')))
    # tFile1 = tPath1 + 'bibleVerses.sql'

    print(tFile1)
    tFile2 = filedialog.askopenfilename(initialdir = tPath2,
                                       title = 'Select file',
                                       filetypes = (('SeQueL files','*.sql'),('TeXT files','*.txt'),('all files','*.*')))
    # tFile2 = 'versesMaster_2.txt'

    # Print confirmation
    print('--------------------------------------------------------------------')
    print('Comparing files ', ' 1: ' + tFile1, ' 2: ' +tFile2, sep='\n')
    print('--------------------------------------------------------------------')

    buffer = ''

    fr1 = open(tFile1, 'r')
    fw = open('comparison.sql', 'w')

    fr2 = open(tFile2, 'r')
    tLine1 = fr1.readline()
    tLine2 = fr2.readline()
    tChap = tLine1[2:5]
    print(tChap)
    while not tLine1[:12] == 'INSERT INTO ':
        tLine1 = fr1.readline()
    # print('################:' + tLine1 + ':################')
    tBook = tLine1[82:85]
    print('\n' + tBook)
    while not tLine2[:12] == 'INSERT INTO ':
        tLine2 = fr2.readline()
    # print('================:' + tLine2 + ':================')

    while tLine1 or tLine2:
        tBookNew = tLine1[82:85]
        if tBookNew != tBook:
            tBook = tBookNew
            print('\n' + tBook)
        if tLine1 == tLine2:
            print('.', end='')
            # fw.write(tLine1)
            fw.write('-')
        else:
            #print('')
            #print('1:' + tLine1)
            #print('2:' + tLine2)
            #iLine = input('1 or 2 (or 3 for new input):')
            #if iLine == 1:
            #    fw.write(tLine1)
            #if iLine == 2:
            #    fw.write(tLine2)
            #if iLine == 3:
            #    newLine = input('New line:')
            #    fw.write(newLine)
            print('D', end='')
            fw.write(tLine1)
            fw.write('--' + tLine2)

        tLine1 = fr1.readline()
        tLine2 = fr2.readline()

    fr1.close()
    fr2.close()
    fw.close()

main()
