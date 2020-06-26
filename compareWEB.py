import os
from bibleModule import lpadNum

#globals
tPath = 'E:\\GitHub\\bookish-lamp\\'
tPath1 = 'eng-web_usfm\\'
tPath2 = 'eng-web_usfm_2020-06-01\\'
fw = ''

def main():
    global fw
    tBook = ''

    fw = open(tPath + 'WEBChanges.txt', 'w', encoding="utf8")
    bOldTestament = True

    os.chdir(tPath + tPath1)
    for tFileName1 in os.listdir(tPath + tPath1):
        if tFileName1.endswith('.usfm'):
            tBookPrev = tBook
            tBook = tFileName1[3:6]
            if tBook=='MAT':
                bOldTestament=False

            tFileName2 = getFileName2(tFileName1)

            compareThem(tFileName1, tFileName2, tBook)
            #wait = input("PRESS ENTER TO CONTINUE.")
    fw.close()
    print('Done!')

def compareThem(tFile1, tFile2, tBook):
    #global fw

    print('--------------------------------------------------------------------')
    print('Comparing ' + tFile1 + ' with ' + tFile2)
    print('--------------------------------------------------------------------')

    fr1 = open(tPath + tPath1 + tFile1, 'r', encoding='utf8')
    fr2 = open(tPath + tPath2 + tFile2, 'r', encoding='utf8')

    tChapter1 = tChapter2 = '1'
    tVerse1 = tVerse2 = ''
    para = ''
    tLine1 = tLine2 = ''
    tBuffer1 = tBuffer2 = ''
    tLine1 = tLine2 = 'start'

    while tLine1 and tLine2:
        #print('@', end='')
        tLine1, tBuffer1 = getToVerseOrChapter(tLine1, tBuffer1, fr1)
        tChapter1, tLine1, tBuffer1 = getChapter(tChapter1, tLine1, tBuffer1)

        tLine2, tBuffer2 = getToVerseOrChapter(tLine2, tBuffer2, fr2)
        tChapter2, tLine2, tBuffer2 = getChapter(tChapter2, tLine2, tBuffer2)

        processLine(tLine1, tLine2, tBook, tChapter1, tChapter2)

        if tBuffer1:
            tLine1 = tBuffer1
            tBuffer1 = ''
        else:
            tLine1 = fr1.readline()

        if tBuffer2:
            tLine2 = tBuffer2
            tBuffer2 = ''
        else:
            tLine2 = fr2.readline()

    fr1.close()
    fr2.close()
    print('--------------------------------------------------------------------')
    print(tFile1 + ' compared with ' + tFile2)
    print('--------------------------------------------------------------------')

def getToVerseOrChapter(tLine, tBuffer, fr):
    if tLine == tBuffer:
        print('Buffer matches line!')
        wait = input("PRESS ENTER TO CONTINUE.")

    if not tBuffer:
        tBuffer = fr.readline()

    if not tLine:
        tline = tBuffer
        tBuffer = fr.readline()

    while tBuffer:
        if tBuffer.startswith('\\c'):
            tLine = tBuffer
            tBuffer = ''
            break
        if tBuffer.startswith('\\v') or tBuffer.startswith('\\p') or tBuffer.startswith('\\q'):
            #print('#', end='')
            tLine = tBuffer
            tBuffer = fr.readline()
            if tBuffer.startswith('\\c'):
                break
            para = ''
            while tLine.startswith('\\p') or tLine.startswith('\\q'):
                para += tLine[3:-1].strip() + ' '
                tLine = tBuffer
                tBuffer = fr.readline()
                if para > '':
                    print('p', end='')
            if tLine.startswith('\\v'):
                while tBuffer.startswith('\\p') or tBuffer.startswith('\\q'):
                    para += tBuffer[3:-1].strip() + ' '
                    tBuffer = fr.readline()
                break
        else:
            tBuffer = fr.readline()

    return tLine, tBuffer

def getChapter(tChapter, tLine, tBuffer):
    if tLine.startswith('\\c'):
        tChapter = lpadNum(tLine[3:-1])
        print('')
        print(' Cl ', end='')
        tLine = tBuffer
        tBuffer = ''
    else:
        if tBuffer.startswith('\\c'):
            tChapter = lpadNum(tBuffer[3:-1])
            tBuffer = ''
            print('')
            print(' Cb ', end='')
    return tChapter, tLine, tBuffer

def processLine(tLine1, tLine2, tBook, tChapter1, tChapter2):
    #global fw
    #print(tLine1[2:5] + tLine2[2:5], end='')

    if tLine1 == tLine2:
        print('.', end='')
    else: 
        print(tLine1)
        print(tLine2)
        #print('*', end='')
        tVerse1 = lpadNum(tLine1[2:5])
        tVerse2 = lpadNum(tLine2[2:5])
        tLine1 = tLine1[5:].strip(' ')
        tLine2 = tLine2[5:].strip(' ')

        fw.write(tBook)
        fw.write(tChapter1 + ':')
        fw.write(tVerse1 + ', ')
        fw.write(tLine1)
        fw.write(tBook)
        fw.write(tChapter2 + ':')
        fw.write(tVerse2 + ', ')
        fw.write(tLine2)

def stuff():
    line = parseSQL(fr1, fw2,"'")
    tLine1 = line[0]
    tBook1Prev = tBook1
    tBook1 = line[1]
    tChapter1 = lpadNum(line[2])
    tVerse1 = lpadNum(line[3])
    tVerse2 = tLine2[2:8].strip()
    tVerse2 = lpadNum(tVerse2[0:tVerse2.find(' ')])
    tLine2 = trimComments(tLine2)
    tLine2 = swapQuotes(firstAlphaOrQuote(tLine2[3:].strip() + ' ' + para))

    tLine2 = swapWords(tLine2, '\\wj*', '')
    tLine2 = swapWords(tLine2, '\\wj ', '')
    tLine2 = swapWords(tLine2, 'wj ', '')

    tLine2 = swapWords(tLine2, 'lamp stand', 'lampstand')
    tLine2 = swapWords(tLine2, 'bondage', 'slavery')
    tLine2 = swapWords(tLine2, 'worshiper', 'worshipper')
    tLine1 = swapWords(tLine1, 'it happened that ', '')
    tLine1 = swapWords(tLine1, 'It happened ', '')
    if bOldTestament:
        tLine2 = swapWords(tLine2, 'Yahweh', 'TheIAM<H3068>')
        tLine2 = swapWords(tLine2, 'herb', 'vegetation<H6212>')
        tLine2 = addCode(tLine2, 'Lord', '<H0113>')
        tLine2 = addCode(tLine2, 'gods', '<H0430>')
        tLine2 = addCode(tLine2, 'god', '<H0430>')
        tLine2 = addCode(tLine2, 'God', '<H0430>')
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

    if tVerse2 != tVerse1:
        x = input(tChapter1 + ':' + tVerse1 + '|' + tChapter2 + ':' + tVerse2)
    if tBook2 != tBook1:
        x = input(tBook1 + 'was' + tBook1Prev + '|' + tBook2 + 'was' + tBook2Prev + '\n' + tLine1 + '|' + tLine2)
        if tBook2 == tBook1Prev:
            print('skipping:' + tLine2, end='')
            tLine2 = fr2.readline()
        else:
            x = input(tBook1 + 'was' + tBook1Prev + '|' + tBook2 + 'was' + tBook2Prev)
            if x == 1:
                line = parseSQL(fr1, fw2, "'")
                tLine1 = line[0]
                tBook1Prev = tBook1
                tBook1 = line[1]
                tChapter1 = line[2]
                tVerse1 = line[3]
            if x == 2:
                tLine2 = fr2.readline()
    if tLine1 == tLine2:
        fw2.write(line[4])
        #fw2.write('(same)')
    else:
        tLine2 = escapeQuotes(tLine2, '\"')
        tLine2 = escapeQuotes(tLine2, '\'')
        #x = input(tLine1 + '|||' + tLine2)
        fw1.write('(\'' + tBook1 + '\',' + tChapter1 + ',' + tVerse1 + ', \'' + tLine1 + '\'),\n')
        fw2.write('(\'' + tBook2 + '\',' + tChapter2 + ',' + tVerse2 + ', \'' + tLine2.strip() + '\'),\n')
    print('crap dummy line!!!! #########################################')

def getFileName2(tFileName1):
    tFileName2 = tFileName1
    if tFileName1 == '10-1SMeng-web.usfm':
        tFileName2 = '10-1SAeng-web.usfm'
    if tFileName1 == '11-2SMeng-web.usfm':
        tFileName2 = '11-2SAeng-web.usfm'
    if tFileName1 == '23-SONeng-web.usfm':
        tFileName2 = '23-SNGeng-web.usfm'
    if tFileName1 == '27-EZEeng-web.usfm':
        tFileName2 = '27-EZKeng-web.usfm'
    if tFileName1 == '30-JOEeng-web.usfm':
        tFileName2 = '30-JOLeng-web.usfm'
    if tFileName1 == '35-NAHeng-web.usfm':
        tFileName2 = '35-NAMeng-web.usfm'
    if tFileName1 == '71-MAReng-web.usfm':
        tFileName2 = '71-MRKeng-web.usfm'
    if tFileName1 == '73-JOHeng-web.usfm':
        tFileName2 = '73-JHNeng-web.usfm'
    if tFileName1 == '89-JAMeng-web.usfm':
        tFileName2 = '89-JASeng-web.usfm'
    if tFileName1 == '92-1JOeng-web.usfm':
        tFileName2 = '92-1JNeng-web.usfm'
    if tFileName1 == '93-2JOeng-web.usfm':
        tFileName2 = '93-2JNeng-web.usfm'
    if tFileName1 == '94-3JOeng-web.usfm':
        tFileName2 = '94-3JNeng-web.usfm'
    if tFileName1 == '95-JDEeng-web.usfm':
        tFileName2 = '95-JUDeng-web.usfm'
    return tFileName2

main()
