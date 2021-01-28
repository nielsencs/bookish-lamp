import os
from bibleModule import *

def main():
    tBook = ''
    tChapter = ''
    tVerseNum = ''
    tVerseText = ''

    tPath1 = 'WEB(2011)'
    tPath2 = tPath1 + '\\Genesis'

    fw2 = open('WEB(2011)bible.sql', 'w')

    for tFilename in os.listdir(tPath2):
        print('Processing '+ tFilename, end = '')

        tBook = myBookAbbrFromWEBName(tFilename)
        tChapter = getChapterFromFilename(tFilename)
        tChapter = tChapter.zfill(5)

        fr2 = open(tPath2 + '\\' + tFilename, 'r')
        tBuffer = fr2.readline()
        while tBuffer:
            tVerseNum, tVerseText = getVerse(tBuffer)
            tVerseText = escapeQuotes(tVerseText, '\"')
            tVerseText = escapeQuotes(tVerseText, '\'')

            fw2.write('INSERT INTO `verses` (`bookCode`, `chapter`, `verseNumber`, `verseText`) VALUES ')
            fw2.write('(\'' + tBook + '\',' + tChapter + ',' + tVerseNum + ', \'' + tVerseText.strip() + '\');\n')

            print('.', end = '') # show progress

            tBuffer = fr2.readline()
        print('')

def getChapterFromFilename(tFilename):
    tChapter = tFilename[-7:-4]
    if tChapter[0].isalpha():
        tChapter = ' ' + tChapter[1:].zfill(4)
    return tChapter

def getVerse(tBuffer):
    i = tBuffer.index(' ')
    tVerseNum = ' ' + tBuffer[0:i].zfill(4)
    tVerseText = tBuffer[i:]
    return tVerseNum, tVerseText

main()
