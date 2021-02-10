import os
from bibleModule import *

def main():
    tPath1 = 'eng-web_usfm_2020-09-09'

    para = ''
    tLine2 = ''
    buffer = ''

    comStart = '\\f'
    comEnd = '\\f*'
    com2Start = '\\x'
    com2End = '\\x*'

    tPath2 = 'generatedSQL'
    fw2 = open(tPath2 + '\\USFM_2020-09-09_bible.sql', 'w', encoding="utf8")

    bOldTestament = True
    tBook2 = ''
    tChapter2 = ''
    tVerseNum = ''
    tVerseText = ''

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
                fr2 = open(tPath1 + '\\' +filename, 'r', encoding="utf8")

                buffer = getLine(fr2)
                while buffer:
                    if buffer.startswith('\\v') or buffer.startswith('\\c') or buffer.startswith('\\d') or buffer.startswith('\\p') or buffer.startswith('\\q') or buffer.startswith('\\ms1'):
                        tLine2 = buffer
                        buffer = getLine(fr2)
                        if tLine2.startswith('\\ms1'): #psalm books
                            tVerse2 = lpadNum('0')
                            tLine2 = '[' + tLine2[5:].strip() + ']'
                            if buffer.startswith('\\d'):
                                tLine2 = tLine2 + ' ' + buffer[3:].strip()
                                # buffer = getLine(fr2)
                            writeLine(fw2, tBook2, tChapter2, tVerse2, tLine2)
                            buffer = getLine(fr2)
                        if tLine2.startswith('\\d'):
                            tVerse2 = lpadNum('0')
                            tLine2 = tLine2[3:].strip()
                            writeLine(fw2, tBook2, tChapter2, tVerse2, tLine2)
                            buffer = getLine(fr2)
                        if tLine2.startswith('\\c'):
                            tChapter2 = lpadNum(tLine2[3:-1])
                        para = ''
                        while tLine2.startswith('\\p') or tLine2.startswith('\\q'):
                            para += tLine2[3:-1].strip() + ' '
                            tLine2 = buffer
                            buffer = getLine(fr2)
                            if para > '':
                                print('p', end='')

                        if tLine2.startswith('\\v'):
                            while buffer.startswith('\\p') or buffer.startswith('\\q'):
                                para += buffer[3:-1].strip() + ' '
                                buffer = getLine(fr2)
                            tVerse2 = tLine2[2:8].strip()
                            tVerse2 = lpadNum(tVerse2[0:tVerse2.find(' ')])

                            tLine2 = swapQuotes(firstAlphaOrQuote(tLine2[3:].strip() + ' ' + para))

                            if comStart in tLine2:
                                tLine2=trimExtras(tLine2, comStart, comEnd)
                                print('+', end='')
                            else:
                                print('-', end='')

                            if com2Start in tLine2:
                                tLine2=trimExtras(tLine2, com2Start, com2End)
                                print('#', end='')
                            else:
                                print('-', end='')

                            tLine2 = swapWords(tLine2, '\\wj*', '')
                            tLine2 = swapWords(tLine2, '\\wj ', '')
                            tLine2 = swapWords(tLine2, 'wj ', '')

                            tLine2 = swapWords(tLine2, 'lamp stand', 'lampstand')
                            tLine2 = swapWords(tLine2, 'bondage', 'slavery')
                            tLine2 = swapWords(tLine2, 'worshiper', 'worshipper')
                            tLine2 = swapWords(tLine2, 'seed', 'offspring')
                            tLine2 = swapWords(tLine2, 'chastening', 'discipline')

                            if bOldTestament:
                                tLine2 = swapWords(tLine2, 'Yahweh', 'TheIAM<H3068>')
                                tLine2 = swapWords(tLine2, 'herb', 'vegetation<H6212>')
                                tLine2 = addCode(tLine2, 'Lord', '<H0113>')
                                tLine2 = addCode(tLine2, 'lord', '<H0113>')
                                tLine2 = addCode(tLine2, 'gods', '<H0430>')
                                tLine2 = addCode(tLine2, 'god', '<H0430>')
                                tLine2 = addCode(tLine2, 'God', '<H0430>')
                                tLine2 = addCode(tLine2, 'anointed', '<H4886>')
                                tLine2 = addCode(tLine2, 'Almighty', '<H7706>')
                                tLine2 = addCode(tLine2, 'pursue', '<H7291>')
                                tLine2 = addCode(tLine2, 'persecute', '<H7291>')
                            else:
                                tLine2 = swapWords(tLine2, 'Christ', 'AnointedOne<G5547>')

                                tLine2 = swapWords(tLine2, 'beloved', 'dear-ones<G0027>')
                                tLine2 = swapWords(tLine2, 'Beloved', 'Dear-ones<G0027>')

                                tLine2 = addCode(tLine2, 'Lord', '<G2962>')
                                tLine2 = addCode(tLine2, 'lord', '<G2962>')
                                tLine2 = addCode(tLine2, 'love', '<G0025>')

                                tLine2 = swapWords(tLine2, 'love<G0025>d', 'loved<G0025>')
                                tLine2 = swapWords(tLine2, 'love<G0025>s', 'loves<G0025>')
                                tLine2 = swapWords(tLine2, 'is love<G0025>', 'is love<G0026>')
                                tLine2 = swapWords(tLine2, 'God\'s love<G0025>', 'God\'s love<G0026>')
                                tLine2 = swapWords(tLine2, 'a love<G0025>', 'a love<G0026>')

                                tLine2 = addCode(tLine2, 'master', '<G2962>')
                                tLine2 = addCode(tLine2, 'Master', '<G2962>')
                                tLine2 = swapWords(tLine2, 'master<G2962>s', 'masters<G2962>')
                                tLine2 = swapWords(tLine2, 'Master<G2962>s', 'Masters<G2962>')
                                tLine2 = swapWords(tLine2, 'master<G2962>\'s', 'master\'s<G2962>')

                                tLine2 = swapWords(tLine2, 'works', 'acts')

                            tLine2 = swapWords(tLine2, '—', '- ')
                            tLine2 = swapWords(tLine2, '  ', ' ')
                            tLine2 = tLine2.strip()

                            tLine2 = escapeQuotes(tLine2, '\"')
                            tLine2 = escapeQuotes(tLine2, '\'')
                            #x = input(tLine1 + '|||' + tLine2)

                            writeLine(fw2, tBook2, tChapter2, tVerse2, tLine2)
                        else:
                            print('.', end='')
                    else:
                        buffer = getLine(fr2)
                fr2.close()
                print('')
    fw2.close()

main()
