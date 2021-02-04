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
    bOldTestament = True
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

            if tBook == 'MAT':
                bOldTestament = False
            fr2 = open(tPath1 + '\\' + tPath2 + '\\' + tFilename, 'r')
            tBuffer = fr2.readline()
            while tBuffer:
                tVerseNum, tVerseText = getVerse(tBuffer)
                tVerseText = escapeQuotes(tVerseText, '\"')
                tVerseText = escapeQuotes(tVerseText, '\'')

                tVerseText = swapWords(tVerseText, 'lamp stand', 'lampstand')
                tVerseText = swapWords(tVerseText, 'bondage', 'slavery')
                tVerseText = swapWords(tVerseText, 'worshiper', 'worshipper')
                tVerseText = swapWords(tVerseText, 'seed', 'offspring')
                tVerseText = swapWords(tVerseText, 'chastening', 'discipline')

                if bOldTestament:
                    tVerseText = swapWords(tVerseText, 'Yahweh', 'TheIAM<H3068>')
                    tVerseText = swapWords(tVerseText, 'herb', 'vegetation<H6212>')
                    tVerseText = addCode(tVerseText, 'Lord', '<H0113>')
                    tVerseText = addCode(tVerseText, 'lord', '<H0113>')
                    tVerseText = addCode(tVerseText, 'gods', '<H0430>')
                    tVerseText = addCode(tVerseText, 'god', '<H0430>')
                    tVerseText = addCode(tVerseText, 'God', '<H0430>')
                    tVerseText = addCode(tVerseText, 'anointed', '<H4886>')
                    tVerseText = addCode(tVerseText, 'Almighty', '<H7706>')
                    tVerseText = addCode(tVerseText, 'pursue', '<H7291>')
                    tVerseText = addCode(tVerseText, 'persecute', '<H7291>')
                else:
                    tVerseText = swapWords(tVerseText, 'Christ', 'AnointedOne<G5547>')

                    tVerseText = swapWords(tVerseText, 'beloved', 'dear-ones<G0027>')
                    tVerseText = swapWords(tVerseText, 'Beloved', 'Dear-ones<G0027>')

                    tVerseText = addCode(tVerseText, 'Lord', '<G2962>')
                    tVerseText = addCode(tVerseText, 'lord', '<G2962>')
                    tVerseText = addCode(tVerseText, 'love', '<G0025>')

                    tVerseText = swapWords(tVerseText, 'love<G0025>d', 'loved<G0025>')
                    tVerseText = swapWords(tVerseText, 'love<G0025>s', 'loves<G0025>')
                    tVerseText = swapWords(tVerseText, 'is love<G0025>', 'is love<G0026>')
                    tVerseText = swapWords(tVerseText, 'God\'s love<G0025>', 'God\'s love<G0026>')
                    tVerseText = swapWords(tVerseText, 'a love<G0025>', 'a love<G0026>')

                    tVerseText = addCode(tVerseText, 'master', '<G2962>')
                    tVerseText = addCode(tVerseText, 'Master', '<G2962>')
                    tVerseText = swapWords(tVerseText, 'master<G2962>s', 'masters<G2962>')
                    tVerseText = swapWords(tVerseText, 'Master<G2962>s', 'Masters<G2962>')
                    tVerseText = swapWords(tVerseText, 'master<G2962>\'s', 'master\'s<G2962>')

                    tVerseText = swapWords(tVerseText, 'works', 'acts')

                tVerseText = swapWords(tVerseText, '—', '- ')
                tVerseText = swapWords(tVerseText, '  ', ' ')
                tVerseText = tVerseText.strip()


                fw2.write('INSERT INTO `verses` (`bookCode`, `chapter`, `verseNumber`, `verseText`) VALUES ')
                fw2.write('(\'' + tBook + '\',' + tChapter + ',' + tVerseNum + ', \'' + tVerseText.strip() + '\');\n')

                print('.', end = '') # show progress

                tBuffer = fr2.readline()
            print('')

def getChapterFromFilename(tFilename):
    tChapter = tFilename[-7:-4]
    while tChapter[0].isalpha() or tChapter[0] == '0': # strip leading spaces or 0s
        tChapter = tChapter[1:]
    tChapter = lpadNum(tChapter)

    return tChapter

def getVerse(tBuffer):
    i = tBuffer.index(' ')

    tVerseNum = tBuffer[0:i].strip()
    if tVerseNum[0] == '0': # strip leading 0
        tVerseNum = tVerseNum[1:]
    if tVerseNum == '': #was 0!
        tVerseNum = '0'
    tVerseNum = lpadNum(tVerseNum)
    tVerseText = tBuffer[i:]
    return tVerseNum, tVerseText

main()
