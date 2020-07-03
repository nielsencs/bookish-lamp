import os
from bibleModule import *

def main():
    tPath1 = 'E:\\GitHub\\bookish-lamp\\structure'
    tPath2 = 'E:\\GitHub\\bookish-lamp\\eng-web_usfm_2020-06-01'
    tBook1 = ''
    tBook2 = ''
    tBook1Prev = ''
    tBook2Prev = ''
    tChapter1 = ''
    tChapter2 = ''
    tVerse1 = ''
    tVerse2 = ''
    para = ''
    tLine1 = ''
    tLine2 = ''
    buffer = ''

    comStart = '\\f'
    comEnd = '\\f*'
    com2Start = '\\x'
    com2End = '\\x*'

    os.chdir(tPath1)
    fr1 = open('versesMaster.sql', 'r')
    os.chdir(tPath2)
    fw1 = open('..\\versesMaster_1.txt', 'w', encoding="utf8")
    fw2 = open('..\\versesMaster_2.txt', 'w', encoding="utf8")
    bOldTestament = True

    doHeader(fw1)
    
    for filename in os.listdir(tPath2):
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
                    tLine2 = buffer
                    buffer = fr2.readline()
                    if tLine2.startswith('\\c'):
                        tChapter2 = lpadNum(tLine2[3:-1])
                    para = ''
                    while tLine2.startswith('\\p') or tLine2.startswith('\\q'):
                        para += tLine2[3:-1].strip() + ' '
                        tLine2 = buffer
                        buffer = fr2.readline()
                        if para > '':
                            print('p', end='')
                    if tLine2.startswith('\\v'):
                        while buffer.startswith('\\p') or buffer.startswith('\\q'):
                            para += buffer[3:-1].strip() + ' '
                            buffer = fr2.readline()
                        line = parseSQL(fr1, fw2,"'")
                        tLine1 = line[0]
                        tBook1Prev = tBook1
                        tBook1 = line[1]
                        tChapter1 = lpadNum(line[2])
                        tVerse1 = lpadNum(line[3])
                        tVerse2 = tLine2[2:8].strip()
                        tVerse2 = lpadNum(tVerse2[0:tVerse2.find(' ')])

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
    tLine1Clean = ''
    tBook = ''
    tChapter = ''
    tVerse = ''
    
    bDoIt = True
    while bDoIt:
        tLine1SQL = fr1.readline()
        if tLine1SQL[0:6] == 'INSERT':
            print('I', end='')
            fw2.write(tLine1SQL)
        elif tLine1SQL[13:16].strip() == '0':
            print('0', end='')
            fw2.write(tLine1SQL)
        else:
            if tVerseDelim in tLine1SQL:
                bDoIt = False
                tBook = tLine1SQL[2:5]
                tChapter = tLine1SQL[8:11]
                tVerse = tLine1SQL[13:16]
                tLine1Clean = tLine1SQL[15:]
                tLine1Clean = tLine1Clean[tLine1Clean.find(tVerseDelim)+1:-4]
                tLine1Clean = trimAngleBrackets(tLine1Clean)
                tLine1Clean = trimChar(tLine1Clean, '\\')
            else:
                fw2.write(tLine1SQL)
    return tLine1Clean, tBook, tChapter, tVerse, tLine1SQL

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
