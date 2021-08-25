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

tPath1 = 'generatedSQL'
tPath2 = 'database'

tFileReadWNow = 'USFM_2021-08-18_bible'
tExtGuessedStrongs = '0.sql'
tExtUSFM___Strongs = '1.sql'
tExtPlainNoStrongs = 'NS.sql'

tFileReadOrig = 'WEB(2011)bible'

tTkFileOrig.set(tFileReadOrig + tExtPlainNoStrongs)
tTkFileMine.set('bibleVerses.sql')
tTkFileWNow.set(tFileReadWNow + tExtPlainNoStrongs)

fw = ''
tBook = ''
bStarted = False

tLine1 = ''
tLine2 = ''
# tLine3 = ''
# ==============================================================================
def main():
# ==============================================================================
    setupTopFrame(tTkFileOrig, tTkFileWNow, tTkFileMine)
    setupMidFrame(tTkLine1, bTkLine1, tTkLine2, bTkLine2, tTkLine3, bTkLine3, tTkLine4)

    oTkWindow.mainloop()

    processStop()
# ==============================================================================
def processSame(tLine1, tLine2):
# ==============================================================================
    global tFileReadWNow
    global fr2
    global fw
    global tBook

    while tLine1 == tLine2:
        print('.', end='')
        fw.write(tLine1)
        tBookNew = tLine1[82:85]
        if tBookNew != tBook:
            tBook = tBookNew
            print('\n' + tBook)
        tLine1 = tFileReadWNow.readline()
        tLine2 = fr2.readline()

    tTkLine1.set(tLine1[80:])
    tTkLine2.set(tLine2[80:])
    copyLine()
# ==============================================================================
def copyLine():
# ==============================================================================
    if bTkLine1.get():
        tTkLine3.set(tTkLine1.get())
    if bTkLine2.get():
        tTkLine3.set(tTkLine2.get())
# ==============================================================================
def processStop():
# ==============================================================================
    global tFileReadWNow
    global fr2
    global fw
    global bStarted

    if bStarted:
        tFileReadWNow.close()
        fr2.close()
        fw.close()
# ==============================================================================
def writeFileName(tFile1, tFile2, tPath):
# ==============================================================================
    bDoIt = True
    i = 0
    tI = ''
    while bDoIt:
        tWriteName = ''
        tWriteName = tWriteName + os.path.basename(tFile1)[:-4]
        tWriteName = tWriteName + '-C-'
        tWriteName = tWriteName + os.path.basename(tFile2)[:-4]
        tWriteName = tWriteName + tI
        tWriteName = tWriteName + '.sql'
        if os.path.isfile(tPath + '\\' + tWriteName):
            i = i + 1
            tI = '(' + str(i) + ')'
        else:
            bDoIt = False
    return tPath + '\\' + tWriteName
# ==============================================================================
def startSession():
# ==============================================================================
    global iScriptLine
    global stream
    global p
    global frames
    global MMdata


    p = pyaudio.PyAudio()
    stream = None
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    frames = []
    MMdata = np.zeros((0,3))
    print("* starting recording session for line " + str(iScriptLine + start_line))
# ==============================================================================
def finishSession():
# ==============================================================================
    global iScriptLine
    global stream
    global p
    global frames
    global tWavFiles

    bStart = True

    print("* done recording session for line " + str(iScriptLine + start_line))

    stream.stop_stream()
    stream.close()
    p.terminate()

    frames_with_content = []

    iLen = len(frames)
    # for i in range(EDGE_MARGIN, iLen-EDGE_MARGIN):
    for i in range(EDGE_MARGIN, iLen):
        keepMarginWindowStart = max(0, i - KEEP_MARGIN)
        keepMarginWindowEnd = min(iLen, i + KEEP_MARGIN+1)
        if bKeepPauses and not bStart:
            frames_with_content.append(frames[i])
        elif np.sum(MMdata[keepMarginWindowStart:keepMarginWindowEnd, 2]) >= 1: # if this chunk, or any of its neighbouring chunks, "has content", include it.
            frames_with_content.append(frames[i])
            bStart = False

    # tWavFile = tPath + '/output' + str(iScriptLine) + '.wav' # restore this if you want to go back to just numbered wave files
    tWavFile = tBook + '_' + str(iChapter).zfill(3) + '_' + str(iScriptLine).zfill(3) + '.wav' # chapter and verse named wave files
    tWavFiles = buildWavFileList(tWavFiles, tWavFile, iScriptLine)
    # tWavFiles[iScriptLine] = tWavFile
    writeWaveFile(tPath + '/' + tWavFile, frames_with_content, p.get_sample_size(FORMAT), CHANNELS, FORMAT, RATE)

    stream = None
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

    oChkBttn5 = tk.Checkbutton(oFrameMid, command=copyLine2, variable = bTkLine3)
    oChkBttn5.grid(column = 2, row=iRow, padx = 0, pady = 0)

    iRow = iRow + 1

    oLabel6 = tk.Label(oFrameMid, text='>', justify = 'right')
    oLabel6.grid(column = 0, row=iRow, padx = 5, pady = 5)

    oText6 = tk.Entry(oFrameMid, textvariable = tTkLine4, width = 210)
    oText6.grid(column = 1, row=iRow, padx = 5, pady = 5)

    oBut6 = tk.Button(oFrameMid, command=processWrite, text='Write to File')
    oBut6.grid(column = 3, row=iRow, padx = 5, pady = 5)
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
    global tFile2
    tFile2 = tk.filedialog.askopenfilename(initialdir = tPath1,
                                           title = 'Select file',
                                           filetypes = (('SeQueL files','*.sql'),('TeXT files','*.txt'),('all files','*.*')))
    tTkFileMine.set(os.path.basename(tFile2))
# ==============================================================================
def processStart():
# ==============================================================================
    # global tTkFileOrig
    global tFileReadWNow
    global fr2
    global fw
    global tBook
    global bStarted

    if len(tTkFileOrig.get()) == 0 or len(tTkFileMine.get()) == 0:
        messagebox.showinfo('Alert', 'Please select files first')
    else:
        buffer = ''

        # tWriteName = writeFileName(tFile1, tFile2, 'database')
        tWriteName = 'database\\combined.sql'
        fw = open(tWriteName, 'w', encoding="utf8")

        tFileReadWNow = open(tFile1, 'r', encoding="utf8")
        tLine1 = tFileReadWNow.readline()
        while not tLine1[:12] == 'INSERT INTO ':
            fw.write(tLine1)
            tLine1 = tFileReadWNow.readline()
        tBook = tLine1[82:85]
        print('\n' + tBook)

        fr2 = open(tFile2, 'r', encoding="utf8")
        tLine2 = fr2.readline()
        while not tLine2[:12] == 'INSERT INTO ':
            tLine2 = fr2.readline()
        processSame(tLine1, tLine2)
        bStarted = True
# ==============================================================================
def copyLine1():
# ==============================================================================
    if bTkLine1.get():
        tTkLine3.set(tTkLine1.get())
        bTkLine2.set(False) # set the other one false
# ==============================================================================
def copyLine2():
# ==============================================================================
    if bTkLine2.get():
        tTkLine3.set(tTkLine2.get())
        bTkLine1.set(False) # set the other one false
# ==============================================================================
def processWrite():
# ==============================================================================
    global tFileReadWNow
    global fr2
    global fw
    global tBook

    print('D', end='')
    fw.write('INSERT INTO `verses` (`bookCode`, `chapter`, `verseNumber`, `verseText`) VALUES ' + tTkLine3.get())

    tLine1 = tFileReadWNow.readline()
    tLine2 = fr2.readline()
    processSame(tLine1, tLine2)
# ------------------------------------------------------------------------------
main()
# ------------------------------------------------------------------------------
