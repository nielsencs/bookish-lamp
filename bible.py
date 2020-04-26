import os

def main():
    path1 = 'E:\\GitHub\\bookish-lamp\\structure'
    path2 = 'E:\\GitHub\\bookish-lamp\\eng-web_usfm'
    tBook1 = ''
    tBook2 = ''
    tBook1Prev = ''
    tBook2Prev = ''
    tChapter1 = ''
    tChapter2 = ''
    tVerse1 = ''
    tVerse2 = ''
    para = ''
    line1 = ''
    line2 = ''
    buffer = ''

    comStart = '\\f'
    comEnd = '\\f*'
    com2Start = '\\x'
    com2End = '\\x*'

    os.chdir(path1)
    fr1 = open('versesMaster.sql', 'r')
    os.chdir(path2)
    fw1 = open('..\\versesMaster_1.txt', 'w', encoding="utf8")
    fw2 = open('..\\versesMaster_2.txt', 'w', encoding="utf8")
    bOldTestament = True

    doHeader(fw1)
    
    for filename in os.listdir(path2):
        if filename.endswith('.usfm'):
            tBook2Prev = tBook2
            tBook2 = filename[3:6]
            if tBook2=='MAT':
                bOldTestament=False
            print('')
            print('processing ' + filename + ':')
            print('')
            fr2 = open(filename, 'r', encoding="utf8")

            buffer = fr2.readline()
            while buffer:
                if buffer.startswith('\\v') or buffer.startswith('\\c') or buffer.startswith('\\p') or buffer.startswith('\\q'):
                    line2 = buffer
                    buffer = fr2.readline()
                    if line2.startswith('\\c'):
                        tChapter2 = lpadNum(line2[3:-1])
                    if line2.startswith('\\p') or line2.startswith('\\q'):
                        para = line2[3:-1].strip()
                        if para > '':
                            print('p', end='')
                    else:
                        para = ''
                    if line2.startswith('\\v'):
                        if buffer.startswith('\\p') or buffer.startswith('\\q'):
                            para = buffer[3:-1].strip()
                            buffer = fr2.readline()
                        line = parseSQL(fr1, fw2,"'")
                        line1 = line[0]
                        tBook1Prev = tBook1
                        tBook1 = line[1]
                        tChapter1 = lpadNum(line[2])
                        tVerse1 = lpadNum(line[3])
                        tVerse2 = line2[2:8].strip()
                        tVerse2 = lpadNum(tVerse2[0:tVerse2.find(' ')])

                        if comStart in line2:
                            line2=line2[0:line2.find(comStart)] + line2[line2.find(comEnd)+3:]
                            print('+', end='')
                        else:
                            print('-', end='')

                        if com2Start in line2:
                            line2=line2[0:line2.find(com2Start)] + line2[line2.find(com2End)+3:]
                            print('#', end='')
                        else:
                            print('-', end='')

                        line2 = swapQuotes(firstAlphaOrQuote(line2[3:].strip() + ' ' + para))

                        line2 = swapWords(line2, '\\wj*', '')
                        line2 = swapWords(line2, '\\wj ', '')
                        line2 = swapWords(line2, 'wj ', '')

                        line2 = swapWords(line2, 'lamp stand', 'lampstand')
                        line2 = swapWords(line2, 'bondage', 'slavery')
                        if bOldTestament:
                            line2 = swapWords(line2, 'Yahweh', 'TheIAM<H3068>')

                            line2 = addCode(line2, 'gods', '<H0430>')
                            line2 = addCode(line2, 'god', '<H0430>')
                            line2 = addCode(line2, 'God', '<H0430>')
                        else:
                            line2 = swapWords(line2, 'Christ', 'AnointedOne<G5547>')
                            line2 = swapWords(line2, 'beloved', 'dear-ones<G0027>')
                            line2 = swapWords(line2, 'Beloved', 'Dear-ones<G0027>')

                            line2 = addCode(line2, 'Lord', '<G2962>')
                            line2 = addCode(line2, 'love', '<G0025>')

                            line2 = swapWords(line2, 'love<G0025>d', 'loved<G0025>')
                            line2 = swapWords(line2, 'love<G0025>s', 'loves<G0025>')
                            line2 = swapWords(line2, 'is love<G0025>', 'is love<G0026>')
                            line2 = swapWords(line2, 'God\'s love<G0025>', 'God\'s love<G0026>')
                            line2 = swapWords(line2, 'a love<G0025>', 'a love<G0026>')

                            line2 = addCode(line2, 'master', '<G2962>')
                            line2 = swapWords(line2, 'master<G2962>s', 'masters<G2962>')
                            line2 = swapWords(line2, 'master<G2962>\'s', 'master\'s<G2962>')
                        line2 = swapWords(line2, '  ', ' ')
                        if tVerse2 != tVerse1:
                            x = input(tChapter1 + ':' + tVerse1 + '|' + tChapter2 + ':' + tVerse2)
                        if tBook2 != tBook1:
                            x = input(tBook1 + 'was' + tBook1Prev + '|' + tBook2 + 'was' + tBook2Prev + '\n' + line1 + '|' + line2)
                            if tBook2 == tBook1Prev:
                                print('skipping:' + line2, end='')
                                line2 = fr2.readline()
                            else:
                                x = input(tBook1 + 'was' + tBook1Prev + '|' + tBook2 + 'was' + tBook2Prev)
                                if x == 1:
                                    line = parseSQL(fr1, fw2, "'")
                                    line1 = line[0]
                                    tBook1Prev = tBook1
                                    tBook1 = line[1]
                                    tChapter1 = line[2]
                                    tVerse1 = line[3]
                                if x == 2:
                                    line2 = fr2.readline()
                        if line1 == line2:
                            fw2.write(line[4])
                            #fw2.write('(same)')
                        else:
                            line2 = escapeQuotes(line2, '\"')
                            line2 = escapeQuotes(line2, '\'')
                            #x = input(line1 + '|||' + line2)
                            fw1.write('(\'' + tBook1 + '\',' + tChapter1 + ',' + tVerse1 + ', \'' + line1 + '\'),\n')
                            fw2.write('(\'' + tBook2 + '\',' + tChapter2 + ',' + tVerse2 + ', \'' + line2.strip() + '\'),\n')
                    else:
                        print('.', end='')
                else:
                    buffer = fr2.readline()
            fr2.close()
            print('')
    fr1.close()
    fw1.close()
    fw2.close()

def parseSQL(fr1, fw2, tVerseDelim):
    line1Clean = ''
    tBook = ''
    tChapter = ''
    tVerse = ''
    
    bDoIt = True
    while bDoIt:
        line1SQL = fr1.readline()
        if line1SQL[0:6] == 'INSERT':
            print('I', end='')
            fw2.write(line1SQL)
        elif line1SQL[13:16].strip() == '0':
            print('0', end='')
            fw2.write(line1SQL)
        else:
            if tVerseDelim in line1SQL:
                bDoIt = False
                tBook = line1SQL[2:5]
                tChapter = line1SQL[8:11]
                tVerse = line1SQL[13:16]
                line1Clean = line1SQL[15:]
                line1Clean = line1Clean[line1Clean.find(tVerseDelim)+1:-4]
                line1Clean = trimAngleBrackets(line1Clean)
                line1Clean = trimChar(line1Clean, '\\')
            else:
                fw2.write(line1SQL)
    return line1Clean, tBook, tChapter, tVerse, line1SQL

def firstAlphaOrQuote(line):
    tQuotes = '“”‘’'
    #print(len(line), end='')
    if len(line)>0:
        bDoIt = True
        while bDoIt:
            if line[0].isalpha() or tQuotes.count(line[0])>0:
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
        
def doHeader(fw2):
    fw2.write('-- phpMyAdmin SQL Dump\n')
    fw2.write('-- version 4.7.0\n')
    fw2.write('-- https://www.phpmyadmin.net/\n')
    fw2.write('--\n')
    fw2.write('-- Host: 127.0.0.1\n')
    fw2.write('-- Generation Time: Mar 01, 2018 at 07:38 PM\n')
    fw2.write('-- Server version: 5.7.17\n')
    fw2.write('-- PHP Version: 5.6.30\n')
    fw2.write('\n')
    fw2.write('SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";\n')
    fw2.write('SET AUTOCOMMIT = 0;\n')
    fw2.write('START TRANSACTION;\n')
    fw2.write('SET time_zone = "+00:00";\n')
    fw2.write('\n')
    fw2.write('\n')
    fw2.write('/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;\n')
    fw2.write('/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;\n')
    fw2.write('/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;\n')
    fw2.write('/*!40101 SET NAMES utf8mb4 */;\n')
    fw2.write('\n')
    fw2.write('--\n')
    fw2.write('-- Database: `biblestu_dy`\n')
    fw2.write('--\n')
    fw2.write('\n')
    fw2.write('-- --------------------------------------------------------\n')
    fw2.write('\n')
    fw2.write('--\n')
    fw2.write('-- Table structure for table `verses`\n')
    fw2.write('--\n')
    fw2.write('\n')
    fw2.write('DROP TABLE IF EXISTS `verses`;\n')
    fw2.write('CREATE TABLE `verses` (\n')
    fw2.write('  `verseID` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,\n')
    fw2.write('  `bookCode` varchar(3) NOT NULL,\n')
    fw2.write('  `chapter` smallint(4) NOT NULL,\n')
    fw2.write('  `verseNumber` smallint(4) NOT NULL,\n')
    fw2.write('  `verseText` text NOT NULL\n')
    fw2.write(') ENGINE=MyISAM DEFAULT CHARSET=latin1;\n')
    fw2.write('\n')
    fw2.write('--\n')
    fw2.write('-- Dumping data for table `verses`\n')
    fw2.write('--\n')
    fw2.write('\n')
    fw2.write('INSERT INTO `verses` (`bookCode`, `chapter`, `verseNumber`, `verseText`) VALUES\n')

main()
