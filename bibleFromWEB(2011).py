import os
from bibleModule import *

atFiles = ['Genesis',
'Exodus',
'Leviticus',
'Numbers',
'Deuteronomy',
'Joshua',
'Judges',
'Ruth',
'1_Samuel',
'2_Samuel',
'1_Kings',
'2_Kings',
'1_Chronicles',
'2_Chronicles',
'Ezra',
'Nehemiah',
'Esther',
'Job',
'Psalms',
'Proverbs',
'Ecclesiastes',
'SongOfSongs',
'Isaiah',
'Jeremiah',
'Lamentations',
'Ezekiel',
'Daniel',
'Hosea',
'Joel',
'Amos',
'Obadiah',
'Jonah',
'Micah',
'Nahum',
'Habakkuk',
'Zephaniah',
'Haggai',
'Zechariah',
'Malachi',
'Matthew',
'Mark',
'Luke',
'John',
'Acts',
'Romans',
'1_Corinthians',
'2_Corinthians',
'Galatians',
'Ephesians',
'Philippians',
'Colossians',
'1_Thessalonians',
'2_Thessalonians',
'1_Timothy',
'2_Timothy',
'Titus',
'Philemon',
'Hebrews',
'James',
'1_Peter',
'2_Peter',
'1_John',
'2_John',
'3_John',
'Jude',
'Revelation']

def main():
    tBook = ''
    tChapter = ''
    tVerseNum = ''
    tVerseText = ''

    tPath1 = 'WEB(2011)'
    fw2 = open('WEB(2011)bible.sql', 'w')
    doHeader(fw2)
    # tPath2 = tPath1 + '\\Genesis'
    # for tPath2 in os.listdir(tPath1): # wrong order!
    for tPath2 in atFiles:
        for tFilename in os.listdir(tPath1 + '\\' + tPath2):
            print('Processing '+ tFilename, end = '')

            tBook = myBookAbbrFromWEBName(tFilename)
            tChapter = getChapterFromFilename(tFilename)

            fr2 = open(tPath1 + '\\' + tPath2 + '\\' + tFilename, 'r')
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
        # tChapter = ' ' + tChapter[1:].zfill(4)
        tChapter = tChapter[1:]
    tChapter = lpadNum(tChapter)

    return tChapter

def getVerse(tBuffer):
    i = tBuffer.index(' ')

    # tVerseNum = ' ' + tBuffer[0:i].zfill(4)
    tVerseNum = tBuffer[0:i]
    tVerseNum = lpadNum(tVerseNum)
    tVerseText = tBuffer[i:]
    return tVerseNum, tVerseText

main()
