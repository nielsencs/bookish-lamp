import os

import tkinter as tk
from tkinter import filedialog

oRoot = tk.Tk()
oRoot.withdraw()

#globals
# tPath1 = 'database\\'
# tPath2 = 'eng-web_usfm_2020-06-01\\'
tPath1 = 'generatedSQL'

def main():
    tFile1 = filedialog.askopenfilename(initialdir = tPath1,
                                       title = 'Select file',
                                       filetypes = (('SeQueL files','*.sql'),('TeXT files','*.txt'),('all files','*.*')))

    print(tFile1)

    tWriteName = writeFileName(tFile1)
    fw = open(tPath1 + '\\' + tWriteName, 'w', encoding="utf8")

    fr1 = open(tFile1, 'r', encoding="utf8")
    tLine1 = fr1.readline()

    while tLine1:
        tLine1, tDot = stripStrongs(tLine1)
        print(tDot, end='')
        fw.write(tLine1)
        tLine1 = fr1.readline()

    fr1.close()
    fw.close()

def writeFileName(tFile1):
    tWriteName = ''
    tWriteName = tWriteName + os.path.basename(tFile1)[:-4]
    tWriteName = tWriteName + 'NS'
    tWriteName = tWriteName + '.sql'
    return tWriteName

def stripStrongs(tLine):
    tStrongStart = '<'
    tStrongEnd = '>'
    tLeft = ''
    tRight = ''
    tDot = '.'
    while tStrongStart in tLine:
        tLeft = tLine[0:tLine.find(tStrongStart)]
        tRight = tLine[tLine.find(tStrongEnd) + 1:]
        tLine = tLeft + tRight
        tDot = 's'
    return tLine, tDot

main()
