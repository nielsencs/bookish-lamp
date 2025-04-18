import os
from bibleModule import doHeader, myBookAbbrFromWEB, notApocrypha, get_line, trimComments, lpadNum, writeLine, swapQuotes, firstAlphaOrQuote, swapWords, addCode, escapeQuotes

import tkinter as tk
from tkinter import filedialog

oTkWindow = tk.Tk()
oTkWindow.withdraw()
oTkWindow.title('Generate SQL from USFM')
oTkWindow.geometry('400x150')
oTkWindow.deiconify()

iAddStrongs = tk.IntVar()
tTkPath1 = tk.StringVar()

tPath1 = 'eng-web-usfm_2021-02-06'
tTkPath1.set(tPath1)

def getPath():
    global tPath1
    tPath1 = tk.filedialog.askdirectory(initialdir = tPath1, title = 'Select USFM folder')
    tTkPath1.set(tPath1)

def main():
    tPath1 = tTkPath1.get()
    print(f"using this folder: '{tPath1}', do", end='')
    if iAddStrongs.get() == 0:
        print('n\'t', end='')
    print(' get strongs numbers from USFM file')
    tFile = 'USFM_' + tPath1[-10:] + '_bible' + str(iAddStrongs.get()) + '.sql'
    print('filename:\'' + tFile + '\'')
    bGetStrongsFromFile = iAddStrongs.get()==1

    para = ''
    tLine2 = ''
    buffer = ''

    tPath2 = 'generatedSQL'

    fw2 = open(os.path.join(tPath2, tFile), 'w', encoding="utf8")

    bOldTestament = True
    tBook2 = ''
    tChapter2 = ''
    tVerse2 = ''
    tLetterText = ''

    doHeader(fw2)

    for filename in os.listdir(tPath1):
        if filename.endswith('.usfm'):
            tBook2 = myBookAbbrFromWEB(filename[3:6])
            if notApocrypha(tBook2):
                if tBook2=='MAT':
                    bOldTestament=False
                print('')
                print('processing ' + filename + ':')
                print('')
                fr2 = open(os.path.join(tPath1, filename), 'r', encoding="utf8")

                buffer = get_line(fr2, bGetStrongsFromFile)
                while buffer:
                    if buffer.startswith('\\v') or buffer.startswith('\\c') or buffer.startswith('\\d') or buffer.startswith('\\p') or buffer.startswith('\\q') or buffer.startswith('\\ms1'):
                        tLine2 = buffer
                        buffer = get_line(fr2, bGetStrongsFromFile)
                        if tLine2.startswith('\\ms1'): #psalm books
                            tVerse2 = lpadNum('0')
                            tLine2 = '[' + tLine2[5:].strip() + ']'
                            if buffer.startswith('\\d'):
                                tLine2 = tLine2 + ' ' + trimComments(buffer[3:].strip())
                                # buffer = get_line(fr2, bGetStrongsFromFile)
                            writeLine(fw2, tBook2, tChapter2, tVerse2, tLine2)
                            buffer = get_line(fr2, bGetStrongsFromFile)
                        if tLine2.startswith('\\d'):
                            if tBook2 == 'PSA' and tChapter2.strip() == '119':
                                tLetterText = '[' + tLine2[3:].strip() + '] '
                            else:
                                tVerse2 = lpadNum('0')
                                tLine2 = trimComments(tLine2[3:].strip())
                                writeLine(fw2, tBook2, tChapter2, tVerse2, tLine2)
                                buffer = get_line(fr2, bGetStrongsFromFile)
                        if tLine2.startswith('\\c'):
                            tChapter2 = lpadNum(tLine2[3:-1])
                        para = ''
                        while tLine2.startswith('\\p') or tLine2.startswith('\\q'):
                            para += tLine2[3:-1].strip() + ' '
                            tLine2 = buffer
                            buffer = get_line(fr2, bGetStrongsFromFile)
                            if para > '':
                                print('p', end='')

                        if tLine2.startswith('\\v'):
                            while buffer.startswith('\\p') or buffer.startswith('\\q'):
                                para += buffer[3:-1].strip() + ' '
                                buffer = get_line(fr2, bGetStrongsFromFile)
                            tVerse2 = tLine2[2:8].strip()
                            tVerse2 = lpadNum(tVerse2[0:tVerse2.find(' ')])

                            tLine2 = swapQuotes(firstAlphaOrQuote(tLine2[3:].strip() + ' ' + para))
                            tLine2 = tLetterText + trimComments(firstAlphaOrQuote(tLine2))
                            tLetterText = ''

                            #============== ignore unhandled tags ==============
                            tLine2 = swapWords(tLine2, '\\wj*', '')
                            tLine2 = swapWords(tLine2, '\\wj ', '')
                            tLine2 = swapWords(tLine2, 'wj ', '')
                            tLine2 = swapWords(tLine2, '\\qs*', '')
                            tLine2 = swapWords(tLine2, '\\qs', '')
                            tLine2 = swapWords(tLine2, '\\bk*', '')
                            tLine2 = swapWords(tLine2, '\\bk', '')
                            #============== ignore unhandled tags ==============

                            tLine2 = swapWords(tLine2, 'lamp stand', 'lampstand')
                            tLine2 = swapWords(tLine2, 'bondage', 'slavery')
                            tLine2 = swapWords(tLine2, 'worshiper', 'worshipper')
                            tLine2 = swapWords(tLine2, 'chastening', 'discipline')

                            if bOldTestament:
                                if bGetStrongsFromFile:
                                    tLine2 = swapWords(tLine2, 'Yahweh', 'ForeverOne') # up to 2024/??/??
                                    tLine2 = swapWords(tLine2, 'YAHWEH', 'ForeverOne') # up to 2024/??/??
                                    tLine2 = swapWords(tLine2, 'Yah', 'EverOne') # up to 2024/??/??
                                    #tLine2 = swapWords(tLine2, 'The LORD', 'ForeverOne')
                                    #tLine2 = swapWords(tLine2, 'the LORD', 'ForeverOne')
                                    #tLine2 = swapWords(tLine2, 'GOD', 'ForeverOne')
                                    #tLine2 = swapWords(tLine2, 'LORD', 'ForeverOne')

                                    tLine2 = swapWords(tLine2, 'herb', 'vegetation')
                                    # tLine2 = swapWords(tLine2, 'Lord', 'MyLord')
                                else:
                                    tLine2 = swapWords(tLine2, 'Yahweh', 'ForeverOne{H3068}') # up to 2024/??/??
                                    tLine2 = swapWords(tLine2, 'YAHWEH', 'ForeverOne{H3068}') # up to 2024/??/??
                                    tLine2 = swapWords(tLine2, 'Yah', 'EverOne{H3050}') # up to 2024/??/??
                                    #tLine2 = swapWords(tLine2, 'The LORD', 'ForeverOne{H3068}')
                                    #tLine2 = swapWords(tLine2, 'the LORD', 'ForeverOne{H3068}')
                                    #tLine2 = swapWords(tLine2, 'GOD', 'ForeverOne{H3068}')
                                    #tLine2 = swapWords(tLine2, 'LORD', 'ForeverOne{H3068}')

                                    tLine2 = swapWords(tLine2, 'herb', 'vegetation{H6212}')
                                    tLine2 = addCode(tLine2, 'Lord', '{H0113}')
                                    tLine2 = addCode(tLine2, 'lord', '{H0113}')
                                    tLine2 = addCode(tLine2, 'gods', '{H0430}')
                                    tLine2 = addCode(tLine2, 'god', '{H0430}')
                                    tLine2 = addCode(tLine2, 'God', '{H0430}')
                                    tLine2 = addCode(tLine2, 'anointed', '{H4886}')
                                    tLine2 = addCode(tLine2, 'Almighty', '{H7706}')
                                    tLine2 = addCode(tLine2, 'pursue', '{H7291}')
                                    tLine2 = addCode(tLine2, 'persecute', '{H7291}')
                                # tLine2 = swapWords(tLine2, 'Lord{H0136}', 'MyLord{H0136}')
                            else: #new testament!
                                tLine2 = swapWords(tLine2, 'Christ', 'AnointedOne{G5547}')

                                tLine2 = swapWords(tLine2, 'beloved', 'dear-ones{G0027}')
                                tLine2 = swapWords(tLine2, 'Beloved', 'Dear-ones{G0027}')

                                if not bGetStrongsFromFile:
                                    tLine2 = addCode(tLine2, 'Lord', '{G2962}')
                                    tLine2 = addCode(tLine2, 'lord', '{G2962}')
                                    tLine2 = addCode(tLine2, 'love', '{G0025}')

                                tLine2 = swapWords(tLine2, 'love{G0025}d', 'loved{G0025}')
                                tLine2 = swapWords(tLine2, 'love{G0025}s', 'loves{G0025}')
                                tLine2 = swapWords(tLine2, 'is love{G0026}', 'is love{G0026}')
                                tLine2 = swapWords(tLine2, 'God\'s love{G0026}', 'God\'s love{G0026}')
                                tLine2 = swapWords(tLine2, 'a love{G0026}', 'a love{G0026}')

                                if not bGetStrongsFromFile:
                                    tLine2 = addCode(tLine2, 'master', '{G2962}')
                                    tLine2 = addCode(tLine2, 'Master', '{G2962}')
                                tLine2 = swapWords(tLine2, 'master{G2962}s', 'masters{G2962}')
                                tLine2 = swapWords(tLine2, 'Master{G2962}s', 'Masters{G2962}')
                                tLine2 = swapWords(tLine2, 'master{G2962}\'s', 'master\'s{G2962}')

                                tLine2 = swapWords(tLine2, 'works', 'acts')

                            tLine2 = swapWords(tLine2, '—', '- ')
                            tLine2 = swapWords(tLine2, '  ', ' ')
                            tLine2 = tLine2.strip()

                            tLine2 = escapeQuotes(tLine2, '\"')
                            tLine2 = escapeQuotes(tLine2, '\'')

                            writeLine(fw2, tBook2, tChapter2, tVerse2, tLine2)
                        else:
                            print('.', end='')
                    else:
                        buffer = get_line(fr2, bGetStrongsFromFile)
                fr2.close()
                print('')
    fw2.close()

oLabel = tk.Label(oTkWindow, text='            ') # noob way of padding!
oLabel.grid(column = 0, row=0)

oLabel = tk.Label(oTkWindow, text='Path')
oLabel.grid(column = 1, row=1)
oText1 = tk.Entry(oTkWindow, textvariable = tTkPath1, width = 40)
oText1.grid(column = 2, row=1)
oBut1 = tk.Button(oTkWindow, command=getPath, text='browse')
oBut1.grid(column = 3, row=1)

oCheck1 = tk.Checkbutton(oTkWindow, text = 'Get strongs numbers from USFM file',
                               variable = iAddStrongs, onvalue = 1, offvalue = 0)
oCheck1.grid(column = 2)

oBut2 = tk.Button(oTkWindow, command=main, text='Go')
oBut2.grid(column = 2)

oTkWindow.mainloop()
