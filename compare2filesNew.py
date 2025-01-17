import os
from bibleModule import *

import tkinter as tk
from tkinter import filedialog

oRoot = tk.Tk()
oRoot.withdraw()

#globals
tPath1 = 'generatedSQL\\'
tPath2 = 'database\\'

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

    tWriteName = writeFileName(tFile1, tFile2)
    fw = open('comparisons\\' + tWriteName, 'w', encoding="utf8")

    fr1 = open(tFile1, 'r', encoding="utf8")
    tLine1 = fr1.readline()
    while not tLine1[:12] == 'INSERT INTO ':
        tLine1 = fr1.readline()
    tBook = tLine1[82:85]
    print('\n' + tBook)

    fr2 = open(tFile2, 'r', encoding="utf8")
    tLine2 = fr2.readline()
    while not tLine2[:12] == 'INSERT INTO ':
        tLine2 = fr2.readline()

    while tLine1 or tLine2:
        tBookNew = tLine1[82:85]
        if tBookNew != tBook:
            tBook = tBookNew
            print('\n' + tBook)
        if tLine1 == tLine2:
            print('.', end='')
            # fw.write(tLine1)
            fw.write('-\n')
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
            # fw.write(tLine1)
            fw.write(tLine2)

        tLine1 = fr1.readline()
        tLine2 = fr2.readline()

    fr1.close()
    fr2.close()
    fw.close()

def writeFileName(tFile1, tFile2):
    tWriteName = ''
    tWriteName = tWriteName + os.path.basename(tFile1)[:-4]
    tWriteName = tWriteName + '-vs-'
    tWriteName = tWriteName + os.path.basename(tFile2)[:-4]
    tWriteName = tWriteName + '.sql'
    return tWriteName

main()
