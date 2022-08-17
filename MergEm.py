import io
import numpy as np
import subprocess
import os
from shutil import copyfile, rmtree

import winsound # error beep!
iFreq = 440  # Frequency in Hz
iTime = 100  # Duration in ms

# import sys
# sys.path.append(r'../')
from bibleModule import *

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

oTkWindow = tk.Tk()
oTkWindow.title('MergEm - Combine Bible Versions')
oTkWindow.geometry('1680x300')
oTkWindow.config(bg='skyblue')

tTkFileOrig = tk.StringVar()
tTkFileMine = tk.StringVar()
tTkFileWNow = tk.StringVar()
tTkLine1 = tk.StringVar()
tTkLine2 = tk.StringVar()
tTkLine3 = tk.StringVar()
tTkLine4 = tk.StringVar()
bTkLine1 = tk.BooleanVar()
bTkLine2 = tk.BooleanVar()
bTkLine3 = tk.BooleanVar()

bTkLine1.set(True)

tPath1 = 'generatedSQL//'
tPath2 = 'database//'

tExt____JustSeQuEl = '.sql'
tExtGuessedStrongs = '0.sql'
tExtUSFM___Strongs = '1.sql'
tExtPlainNoStrongs = 'NS.sql'

tFileReadOrig = 'WEB(2011)bible'
tFileReadMine = 'bibleVerses'
tFileReadWNow = 'USFM_2021-08-18_bible'

tTkFileOrig.set(tFileReadOrig + tExtPlainNoStrongs)
tTkFileMine.set(tFileReadMine + tExt____JustSeQuEl)
tTkFileWNow.set(tFileReadWNow + tExtPlainNoStrongs)

fw = ''
tBook = ''
bStarted = False

tLine1 = ''
tLine2 = ''
tLine3 = ''
# ==============================================================================
def main():
# ==============================================================================
    setupTopFrame(tTkFileOrig, tTkFileWNow, tTkFileMine)
    setupMidFrame(tTkLine1, bTkLine1, tTkLine2, bTkLine2, tTkLine3, bTkLine3, tTkLine4)

    oTkWindow.mainloop()

    processStop()
# ==============================================================================
def setupTopFrame(tTkFileOrig, tTkFileWNow, tTkFileMine):
# ==============================================================================
    oFrameTop = tk.Frame(oTkWindow)
    oFrameTop.grid(row = 0, column = 0, padx = 5, pady = 5)

    iRow = 0

    oLabel0 = tk.Label(oFrameTop, text='Setup')
    oLabel0.grid(column = 0, row=iRow, padx = 5, pady = 5)

    iRow = iRow + 1

    oLabel1 = tk.Label(oFrameTop, text='Files')
    oLabel1.grid(column = 0, row=iRow, padx = 5, pady = 5)

    oText1 = tk.Entry(oFrameTop, textvariable = tTkFileOrig, width = 40)
    oText1.grid(column = 1, row=iRow, padx = 5, pady = 5)

    oBut1 = tk.Button(oFrameTop, command=getFile1, text='browse')
    oBut1.grid(column = 2, row=iRow, padx = 5, pady = 5)

    oText2 = tk.Entry(oFrameTop, textvariable = tTkFileWNow, width = 40)
    oText2.grid(column = 4, row=iRow, padx = 5, pady = 5)

    oBut2 = tk.Button(oFrameTop, command=getFile2, text='browse')
    oBut2.grid(column = 5, row=iRow, padx = 5, pady = 5)

    oText3 = tk.Entry(oFrameTop, textvariable = tTkFileMine, width = 40)
    oText3.grid(column = 7, row=iRow, padx = 5, pady = 5)

    oBut3 = tk.Button(oFrameTop, command=getFile2, text='browse')
    oBut3.grid(column = 8, row=iRow, padx = 5, pady = 5)

    oBut4 = tk.Button(oFrameTop, command=processStart, text='Go')
    oBut4.grid(column = 9, row=iRow, padx = 5, pady = 5)
# ==============================================================================
def setupMidFrame(tTkLine1, bTkLine1, tTkLine2, bTkLine2, tTkLine3, bTkLine3, tTkLine4):
# ==============================================================================
    oFrameMid = tk.Frame(oTkWindow)
    oFrameMid.grid(row = 1, column = 0, padx = 5, pady = 5)

    iRow = 0

    oLabel2 = tk.Label(oFrameMid, text='Process', justify = 'left')
    oLabel2.grid(column = 0, row=iRow, padx = 5, pady = 5)

    iRow = iRow + 1

    oLabel3 = tk.Label(oFrameMid, text='A', justify = 'right')
    oLabel3.grid(column = 0, row=iRow, padx = 5, pady = 5)

    oText3 = tk.Entry(oFrameMid, textvariable = tTkLine1, width = 210)
    oText3.grid(column = 1, row=iRow, padx = 5, pady = 5)

    oChkBttn3 = tk.Checkbutton(oFrameMid, command=copyLine1, variable = bTkLine1)
    oChkBttn3.grid(column = 2, row=iRow, padx = 0, pady = 0)

    iRow = iRow + 1

    oLabel4 = tk.Label(oFrameMid, text='B', justify = 'right')
    oLabel4.grid(column = 0, row=iRow, padx = 5, pady = 5)

    oText4 = tk.Entry(oFrameMid, textvariable = tTkLine2, width = 210)
    oText4.grid(column = 1, row=iRow, padx = 5, pady = 5)

    oChkBttn4 = tk.Checkbutton(oFrameMid, command=copyLine2, variable = bTkLine2)
    oChkBttn4.grid(column = 2, row=iRow, padx = 0, pady = 0)

    iRow = iRow + 1

    oLabel5 = tk.Label(oFrameMid, text='C', justify = 'right')
    oLabel5.grid(column = 0, row=iRow, padx = 5, pady = 5)

    oText5 = tk.Entry(oFrameMid, textvariable = tTkLine3, width = 210)
    oText5.grid(column = 1, row=iRow, padx = 5, pady = 5)

    oChkBttn5 = tk.Checkbutton(oFrameMid, command=copyLine3, variable = bTkLine3)
    oChkBttn5.grid(column = 2, row=iRow, padx = 0, pady = 0)

    iRow = iRow + 1

    oLabel6 = tk.Label(oFrameMid, text='>', justify = 'right')
    oLabel6.grid(column = 0, row=iRow, padx = 5, pady = 5)

    oText6 = tk.Entry(oFrameMid, textvariable = tTkLine4, width = 210)
    oText6.grid(column = 1, row=iRow, padx = 5, pady = 5)

    oBut6 = tk.Button(oFrameMid, command=processWrite, text='Write to File')
    oBut6.grid(column = 3, row=iRow, padx = 5, pady = 5)
# ==============================================================================
def processStart():
# ==============================================================================
    global tFileReadOrig
    global tFileReadMine
    global tFileReadWNow
    global fw
    global tBook
    global bStarted
############################################ FIX THIS! ############################################
    if False: #len(tTkFileOrig.get()) == 0 or len(tTkFileMine.get()) or len(tTkFileWNow.get()) == 0:
        messagebox.showinfo('Alert', 'Please select files first')
    else:
############################################ FIX THIS! ############################################
        buffer = ''

        # tWriteName = 'database\\combined.sql'
        # fw = open(tWriteName, 'w', encoding="utf8")

        tFileReadOrig = open(tPath1 + tTkFileOrig.get(), 'r', encoding="utf8")
        tFileReadMine = open(tPath2 + tTkFileMine.get(), 'r', encoding="utf8")
        tFileReadWNow = open(tPath1 + tTkFileWNow.get(), 'r', encoding="utf8")

        tLine1 = tFileReadOrig.readline()
        while not tLine1[:12] == 'INSERT INTO ':
            # fw.write(tLine1)
            tLine1 = tFileReadOrig.readline()
        tBook = tLine1[82:85]
        print('\n' + tBook)

        tLine2 = tFileReadMine.readline()
        while not tLine2[:12] == 'INSERT INTO ':
            # fw.write(tLine2)
            tLine2 = tFileReadMine.readline()

        tLine3 = tFileReadWNow.readline()
        while not tLine3[:12] == 'INSERT INTO ':
            # fw.write(tLine3)
            tLine3 = tFileReadWNow.readline()

        processSame(tLine1, tLine2, tLine3)
        bStarted = True
# ==============================================================================
def processSame(tLine1, tLine2, tLine3):
# ==============================================================================
    global tFileReadOrig
    global tFileReadMine
    global tFileReadWNow
    global fw
    global tBook

    while tLine1 == tLine2:
        # print('.', end='')
        # fw.write(tLine1)
        tBookNew = tLine1[82:85]
        if tBookNew != tBook:
            tBook = tBookNew
            print('\n' + tBook)
        tLine1 = tFileReadOrig.readline()
        tLine2 = tFileReadMine.readline()
        tLine3 = tFileReadWNow.readline()

    tTkLine1.set(tLine1[80:])
    tTkLine2.set(tLine2[80:])
    tTkLine3.set(tLine3[80:])

    copyLine()
# ==============================================================================
def copyLine():
# ==============================================================================
    if bTkLine1.get():
        tTkLine4.set(tTkLine1.get())
    if bTkLine2.get():
        tTkLine4.set(tTkLine2.get())
    if bTkLine3.get():
        tTkLine4.set(tTkLine3.get())
# ==============================================================================
def processStop():
# ==============================================================================
    global tFileReadOrig
    global tFileReadMine
    global tFileReadWNow
    global fw
    global bStarted

    if bStarted:
        tFileReadOrig.close()
        tFileReadMine.close()
        tFileReadWNow.close()
        # fw.close()
# ==============================================================================
def getFile1():
# ==============================================================================
    global tFile1
    tFile1 = tk.filedialog.askopenfilename(initialdir = tPath1,
                                           title = 'Select file',
                                           filetypes = (('SeQueL files','*.sql'),('TeXT files','*.txt'),('all files','*.*')))
    tTkFileOrig.set(os.path.basename(tFile1))
# ==============================================================================
def getFile2():
# ==============================================================================
    global tFile2
    tFile2 = tk.filedialog.askopenfilename(initialdir = tPath1,
                                           title = 'Select file',
                                           filetypes = (('SeQueL files','*.sql'),('TeXT files','*.txt'),('all files','*.*')))
    tTkFileMine.set(os.path.basename(tFile2))
# ==============================================================================
def getFile3():
# ==============================================================================
    global tFile3
    tFile3 = tk.filedialog.askopenfilename(initialdir = tPath1,
                                           title = 'Select file',
                                           filetypes = (('SeQueL files','*.sql'),('TeXT files','*.txt'),('all files','*.*')))
    tTkFileMine.set(os.path.basename(tFile3))
# ==============================================================================
def copyLine1():
# ==============================================================================
    if bTkLine1.get():
        tTkLine4.set(tTkLine1.get())
        bTkLine2.set(False) # set the other two false
        bTkLine3.set(False) # set the other two false
# ==============================================================================
def copyLine2():
# ==============================================================================
    if bTkLine2.get():
        tTkLine4.set(tTkLine2.get())
        bTkLine1.set(False) # set the other two false
        bTkLine3.set(False) # set the other two false
# ==============================================================================
def copyLine3():
# ==============================================================================
    if bTkLine3.get():
        tTkLine4.set(tTkLine3.get())
        bTkLine1.set(False) # set the other two false
        bTkLine2.set(False) # set the other two false
# ==============================================================================
def processWrite():
# ==============================================================================
    global tFileReadOrig
    global tFileReadMine
    global tFileReadWNow
    global fw
    global tBook

    print('D', end='')
    # fw.write('INSERT INTO `verses` (`bookCode`, `chapter`, `verseNumber`, `verseText`) VALUES ' + tTkLine3.get())

    tLine1 = tFileReadOrig.readline()
    tLine2 = tFileReadMine.readline()
    tLine3 = tFileReadWNow.readline()

    processSame(tLine1, tLine2, tLine3)
# ------------------------------------------------------------------------------
main()
# ------------------------------------------------------------------------------
