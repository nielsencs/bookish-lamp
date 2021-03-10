import os
from bibleModule import *

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

oTkWindow = tk.Tk()
oTkWindow.title('Combine Two Bible Versions')
oTkWindow.geometry('1400x300')
oTkWindow.config(bg='skyblue')

tTkFile1 = tk.StringVar()
tTkFile2 = tk.StringVar()
tTkLine1 = tk.StringVar()
tTkLine2 = tk.StringVar()
tTkLine3 = tk.StringVar()
bTkLine1 = tk.BooleanVar()
bTkLine2 = tk.BooleanVar()

tPath1 = 'generatedSQL'
# ==============================================================================
def getFile1():
# ==============================================================================
    global tFile1
    tFile1 = tk.filedialog.askopenfilename(initialdir = tPath1,
                                           title = 'Select file',
                                           filetypes = (('SeQueL files','*.sql'),('TeXT files','*.txt'),('all files','*.*')))
    tTkFile1.set(os.path.basename(tFile1))
# ==============================================================================
def getFile2():
# ==============================================================================
    global tFile2
    tFile2 = tk.filedialog.askopenfilename(initialdir = tPath1,
                                           title = 'Select file',
                                           filetypes = (('SeQueL files','*.sql'),('TeXT files','*.txt'),('all files','*.*')))
    tTkFile2.set(os.path.basename(tFile2))
# ==============================================================================
def setupTopFrame():
# ==============================================================================
    oFrameTop = tk.Frame(oTkWindow)
    oFrameTop.grid(row = 0, column = 0, padx = 5, pady = 5)

    iRow = 0

    oLabel0 = tk.Label(oFrameTop, text='Setup')
    oLabel0.grid(column = 0, row=iRow, padx = 5, pady = 5)

    iRow = iRow + 1

    oLabel1 = tk.Label(oFrameTop, text='Files')
    oLabel1.grid(column = 0, row=iRow, padx = 5, pady = 5)

    oText1 = tk.Entry(oFrameTop, textvariable = tTkFile1, width = 40)
    oText1.grid(column = 1, row=iRow, padx = 5, pady = 5)

    oBut1 = tk.Button(oFrameTop, command=getFile1, text='browse')
    oBut1.grid(column = 2, row=iRow, padx = 5, pady = 5)

    oText2 = tk.Entry(oFrameTop, textvariable = tTkFile2, width = 40)
    oText2.grid(column = 4, row=iRow, padx = 5, pady = 5)

    oBut2 = tk.Button(oFrameTop, command=getFile2, text='browse')
    oBut2.grid(column = 5, row=iRow, padx = 5, pady = 5)

    oBut3 = tk.Button(oFrameTop, command=processStart, text='Go')
    oBut3.grid(column = 7, row=iRow, padx = 5, pady = 5)
# ==============================================================================
def setupMidFrame():
# ==============================================================================
    oFrameMid = tk.Frame(oTkWindow)
    oFrameMid.grid(row = 1, column = 0, padx = 5, pady = 5)

    iRow = 0

    oLabel2 = tk.Label(oFrameMid, text='Process', justify = 'left')
    oLabel2.grid(column = 0, row=iRow, padx = 5, pady = 5)

    iRow = iRow + 1

    oLabel3 = tk.Label(oFrameMid, text='A', justify = 'right')
    oLabel3.grid(column = 0, row=iRow, padx = 5, pady = 5)

    oText3 = tk.Entry(oFrameMid, textvariable = tTkLine1, width = 140)
    oText3.grid(column = 1, row=iRow, padx = 5, pady = 5)

    oChkBttn3 = tk.Checkbutton(oFrameMid, variable = bTkLine1)
    oChkBttn3.grid(column = 2, row=iRow, padx = 0, pady = 0)

    iRow = iRow + 1

    oLabel4 = tk.Label(oFrameMid, text='B', justify = 'right')
    oLabel4.grid(column = 0, row=iRow, padx = 5, pady = 5)

    oText4 = tk.Entry(oFrameMid, textvariable = tTkLine2, width = 140)
    oText4.grid(column = 1, row=iRow, padx = 5, pady = 5)

    oChkBttn4 = tk.Checkbutton(oFrameMid, variable = bTkLine2)
    oChkBttn4.grid(column = 2, row=iRow, padx = 0, pady = 0)

    iRow = iRow + 1

    oLabel5 = tk.Label(oFrameMid, text='>', justify = 'right')
    oLabel5.grid(column = 0, row=iRow, padx = 5, pady = 5)

    oText5 = tk.Entry(oFrameMid, textvariable = tTkLine3, width = 140)
    oText5.grid(column = 1, row=iRow, padx = 5, pady = 5)

    oBut5 = tk.Button(oFrameMid, command=processWrite, text='Write to File')
    oBut5.grid(column = 3, row=iRow, padx = 5, pady = 5)
# ==============================================================================
def processStart():
# ==============================================================================
    if len(tTkFile1.get()) == 0 or len(tTkFile2.get()) == 0:
        messagebox.showinfo('Alert', 'Please select files first')
    else:
        buffer = ''

        tWriteName = writeFileName(tFile1, tFile2, 'database')
        fw = open(tWriteName, 'w', encoding="utf8")

        fr1 = open(tFile1, 'r', encoding="utf8")
        tLine1 = fr1.readline()
        while not tLine1[:12] == 'INSERT INTO ':
            fw.write(tLine1)
            tLine1 = fr1.readline()
        tBook = tLine1[82:85]
        print('\n' + tBook)

        fr2 = open(tFile2, 'r', encoding="utf8")
        tLine2 = fr2.readline()
        while not tLine2[:12] == 'INSERT INTO ':
            tLine2 = fr2.readline()
        processSame()
# ==============================================================================
def processSame():
# ==============================================================================
    while tLine1 == tLine2:
        print('.', end='')
        fw.write(tLine1)
        tBookNew = tLine1[82:85]
        if tBookNew != tBook:
            tBook = tBookNew
            print('\n' + tBook)
        tLine1 = fr1.readline()
        tLine2 = fr2.readline()

    tTkLine1.set(tLine1)
    tTkLine2.set(tLine2)
# ==============================================================================
def processWrite():
# ==============================================================================
    print('D', end='')
    fw.write(tLine3)

    tLine1 = fr1.readline()
    tLine2 = fr2.readline()
    processSame()
# ==============================================================================
def processStop():
# ==============================================================================
    fr1.close()
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

setupTopFrame()
setupMidFrame()

oTkWindow.mainloop()
