import os

import tkinter as tk
from tkinter import filedialog

oRoot = tk.Tk()
oRoot.withdraw()

#globals
tPath1 = 'E:\\GitHub\\bookish-lamp\\structure\\'
tPath2 = 'E:\\GitHub\\bookish-lamp\\eng-web_usfm\\'

tFile1 = ''
tFile2 = ''

tLine1 = ''
tLine2 = ''

tChap = ''

def main():
    # Ask the user to enter the names of files to compare
    #tFile1 = filedialog.askopenfilename(initialdir = tPath1,
    #                                    title = 'Select file',
    #                                    filetypes = (('SeQueL files','*.sql'),('TeXT files','*.txt'),('all files','*.*')))
    tFile1 = tPath1 + 'versesMaster.sql'

    print(tFile1)
    #tFile2 = filedialog.askopenfilename(initialdir = tPath2,
    #                                    title = 'Select file',
    #                                    filetypes = (('TeXT files','*.txt'),('SeQueL files','*.sql'),('all files','*.*')))
    tFile2 = 'versesMaster_2.txt'

    # Print confirmation
    print('--------------------------------------------------------------------')
    print('Comparing files ', ' 1: ' + tFile1, ' 2: ' +tFile2, sep='\n')
    print('--------------------------------------------------------------------')

    buffer = ''

    #os.chdir(tPath1)
    fr1 = open(tFile1, 'r')
    fw = open(tPath1 + 'versesMaster_new.sql', 'w', encoding='utf8')

    fr2 = open(tFile2, 'r', encoding='utf8')
    tLine1 = fr1.readline()
    tLine2 = fr2.readline()
    tChap = tLine1[2:5]
    #print(tChap)
    while tLine1 or tLine2:
        if tChap != tLine1[2:5]:
            if tLine1[2:5] != 'SER':
                tChap = tLine1[2:5]
                print('')
                print('')
                print(tChap)
                print('')
        
        if tLine1 == tLine2:
            print('.', end='')
            fw.write(tLine1)
            #fw.write('(same)')
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

def firstAlpha(line):
    #print(len(line), end='')
    if len(line)>0:
        bDoIt = True
        while bDoIt:
            if line[0].isalpha():
                bDoIt = False
            else:
                line = line[1:]
                #print('"' + line[0] + '" removed:')
                #print(line)
    return line

def trimChar(line, tChar):
    bDoIt = True
    while bDoIt:
        if tChar in line:
            line = line[0:line.find(tChar)] + line[line.find(tChar)+1:]
            #print('"' + tChar + '" removed:')
            #print(line)
        else:
            bDoIt = False
    return line

def swapQuotes(line):
    tChar1 = '“'    
    tChar2 = '”'    
    tChar3 = '‘'    
    tChar4 = '’'
    bDoIt1 = True
    bDoIt2 = True
    bDoIt3 = True
    bDoIt4 = True
    while bDoIt1 or bDoIt2 or bDoIt3 or bDoIt4:
        if tChar1 in line:
            line = line[0:line.find(tChar1)] + '"' + line[line.find(tChar1)+1:]
        else:
            bDoIt1 = False
        if tChar2 in line:
            line = line[0:line.find(tChar2)] + '"' + line[line.find(tChar2)+1:]
        else:
            bDoIt2 = False
        if tChar3 in line:
            line = line[0:line.find(tChar3)] + "'" + line[line.find(tChar3)+1:]
        else:
            bDoIt3 = False
        if tChar4 in line:
            line = line[0:line.find(tChar4)] + "'" + line[line.find(tChar4)+1:]
        else:
            bDoIt4 = False
    return line

def trimAngleBrackets(line):
    lAngle = '<'
    rAngle = '>'
    bDoIt = True
    while bDoIt:
        if lAngle in line:
            lLine = line[0:line.find(lAngle)]
            #print('left part:')
            #print(lLine)
            rLine = line[line.find(rAngle)+1:]
            #print('right part:')
            #print(rLine)
            line = lLine + rLine
            #print('joined:')
            #print(line)
        else:
            bDoIt = False
    return line

def lpadNum(tNum):
    tNum = '   ' + tNum.strip()
    tNum = tNum[-4:]
    return tNum

def swapWords(tText, tWordOut, tWordIn):
    while tWordOut in tText:
        iStart = tText.find(tWordOut)
        iLength = len(tWordOut)
        tText = tText[0:iStart] + tWordIn + tText[iStart + iLength:]
    return tText
        
def addCode(tText, tWord, tCode):
    tNew = ''
    while tWord in tText:
        iStart = tText.find(tWord)
        iLength = len(tWord)
        tNew = tNew + tText[0:iStart + iLength] + tCode
        tText =  tText[iStart + iLength:]
    return tNew + tText
        
def escapeQuotes(tText, tQuote):
    tNew = ''
    while tQuote in tText:
        iStart = tText.find(tQuote)
        tNew = tNew + tText[0:iStart] + '\\' + tQuote
        tText =  tText[iStart + 1:]
    return tNew + tText
        
main()
