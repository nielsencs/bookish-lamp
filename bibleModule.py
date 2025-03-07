import os

def trimComments(t_line):
    comStart = '\\f'
    comEnd = '\\f*'
    com2Start = '\\x'
    com2End = '\\x*'
    if comStart in t_line:
        t_line=trimExtras(t_line, comStart, comEnd)
        print('+', end='')
    else:
        print('-', end='')

    if com2Start in t_line:
        t_line=trimExtras(t_line, com2Start, com2End)
        print('#', end='')
    else:
        print('-', end='')
    return t_line

def trimExtras(t_line, lDelim, rDelim):
    while lDelim in t_line:
        t_left = t_line[0:t_line.find(lDelim)]
        t_right = t_line[t_line.find(rDelim)+3:]
        t_line = t_left + t_right
    return t_line

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

def swapQuotes(line): #now swapping for nothing
    tChar1 = '“'
    tChar2 = '”'
    tChar3 = '‘'
    tChar4 = '’'

    tNewChar1 = '' # "'"
    tNewChar2 = '' # '"'

    bDoIt1 = True
    bDoIt2 = True
    bDoIt3 = True
    bDoIt4 = True
    while bDoIt1 or bDoIt2 or bDoIt3 or bDoIt4:
        if tChar1 in line:
            line = line[0:line.find(tChar1)] + tNewChar2 + line[line.find(tChar1)+1:]
        else:
            bDoIt1 = False
        if tChar2 in line:
            line = line[0:line.find(tChar2)] + tNewChar2 + line[line.find(tChar2)+1:]
        else:
            bDoIt2 = False
        if tChar3 in line:
            line = line[0:line.find(tChar3)] + tNewChar1 + line[line.find(tChar3)+1:]
        else:
            bDoIt3 = False
        if tChar4 in line:
            line = line[0:line.find(tChar4)] + tNewChar1 + line[line.find(tChar4)+1:]
        else:
            bDoIt4 = False
    return line

def trimAngleBrackets(line):
    lAngle = '<'
    rAngle = '>'
    bDoIt = True
    while bDoIt:
        if lAngle in line:
            t_left = line[0:line.find(lAngle)]
            #print('left part:')
            #print(t_left)
            t_right = line[line.find(rAngle)+1:]
            #print('right part:')
            #print(t_right)
            line = t_left + t_right
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
        # bShouldChange = not tCode in tText[iStart + iLength:iStart + iLength + 10] # if there is already that code applied
        # if bShouldChange:
        tTestText = tText[iStart + iLength:iStart + iLength + 1]
        bShouldChange = not tTestText.isalpha() # if the next character is not alpha (e.g space or punctuation)
        if bShouldChange:
            tNew = tNew + tText[0:iStart + iLength] + tCode
            tText =  tText[iStart + iLength:]
        else:
            tNew = tNew + tText[0:iStart + iLength]
            tText =  tText[iStart + iLength:]
    return tNew + tText

def escapeQuotes(tText, tQuote):
    tNew = ''
    while tQuote in tText:
        iStart = tText.find(tQuote)
        tNew = tNew + tText[0:iStart] + '\\' + tQuote
        tText =  tText[iStart + 1:]
    return tNew + tText

def myBookAbbrFromWEB(tBookAbbr):
    tMyBookAbbr = tBookAbbr
    if tBookAbbr == '1SA':
        tMyBookAbbr = '1SM'
    if tBookAbbr == '2SA':
        tMyBookAbbr = '2SM'
    if tBookAbbr == 'SNG':
        tMyBookAbbr = 'SON'
    if tBookAbbr == 'EZK':
        tMyBookAbbr = 'EZE'
    if tBookAbbr == 'JOL':
        tMyBookAbbr = 'JOE'
    if tBookAbbr == 'NAM':
        tMyBookAbbr = 'NAH'
    if tBookAbbr == 'MRK':
        tMyBookAbbr = 'MAR'
    if tBookAbbr == 'JHN':
        tMyBookAbbr = 'JOH'
    if tBookAbbr == 'JAS':
        tMyBookAbbr = 'JAM'
    if tBookAbbr == '1JN':
        tMyBookAbbr = '1JO'
    if tBookAbbr == '2JN':
        tMyBookAbbr = '2JO'
    if tBookAbbr == '3JN':
        tMyBookAbbr = '3JO'
    if tBookAbbr == 'JUD':
        tMyBookAbbr = 'JDE'
    return tMyBookAbbr

def myBookAbbrFromWEBName(tWEBName):
    tWEBName = tWEBName[:-4]
    while tWEBName[-1].isdigit():
        tWEBName = tWEBName[:-1]
    tMyBookAbbr = ''
    if tWEBName == '1_Chronicles':
        tMyBookAbbr = '1CH'
    elif tWEBName == '1_Corinthians':
        tMyBookAbbr = '1CO'
    elif tWEBName == '1_John':
        tMyBookAbbr = '1JO'
    elif tWEBName == '1_Kings':
        tMyBookAbbr = '1KI'
    elif tWEBName == '1_Peter':
        tMyBookAbbr = '1PE'
    elif tWEBName == '1_Samuel':
        tMyBookAbbr = '1SM'
    elif tWEBName == '1_Thessalonians':
        tMyBookAbbr = '1TH'
    elif tWEBName == '1_Timothy':
        tMyBookAbbr = '1TI'
    elif tWEBName == '2_Chronicles':
        tMyBookAbbr = '2CH'
    elif tWEBName == '2_Corinthians':
        tMyBookAbbr = '2CO'
    elif tWEBName == '2_John':
        tMyBookAbbr = '2JO'
    elif tWEBName == '2_Kings':
        tMyBookAbbr = '2KI'
    elif tWEBName == '2_Peter':
        tMyBookAbbr = '2PE'
    elif tWEBName == '2_Samuel':
        tMyBookAbbr = '2SM'
    elif tWEBName == '2_Thessalonians':
        tMyBookAbbr = '2TH'
    elif tWEBName == '2_Timothy':
        tMyBookAbbr = '2TI'
    elif tWEBName == '3_John':
        tMyBookAbbr = '3JO'
    elif tWEBName == 'Acts':
        tMyBookAbbr = 'ACT'
    elif tWEBName == 'Amos':
        tMyBookAbbr = 'AMO'
    elif tWEBName == 'Colossians':
        tMyBookAbbr = 'COL'
    elif tWEBName == 'Daniel':
        tMyBookAbbr = 'DAN'
    elif tWEBName == 'Deuteronomy':
        tMyBookAbbr = 'DEU'
    elif tWEBName == 'Ecclesiastes':
        tMyBookAbbr = 'ECC'
    elif tWEBName == 'Ephesians':
        tMyBookAbbr = 'EPH'
    elif tWEBName == 'Esther':
        tMyBookAbbr = 'EST'
    elif tWEBName == 'Exodus':
        tMyBookAbbr = 'EXO'
    elif tWEBName == 'Ezekiel':
        tMyBookAbbr = 'EZE'
    elif tWEBName == 'Ezra':
        tMyBookAbbr = 'EZR'
    elif tWEBName == 'Galatians':
        tMyBookAbbr = 'GAL'
    elif tWEBName == 'Genesis':
        tMyBookAbbr = 'GEN'
    elif tWEBName == 'Habakkuk':
        tMyBookAbbr = 'HAB'
    elif tWEBName == 'Haggai':
        tMyBookAbbr = 'HAG'
    elif tWEBName == 'Hebrews':
        tMyBookAbbr = 'HEB'
    elif tWEBName == 'Hosea':
        tMyBookAbbr = 'HOS'
    elif tWEBName == 'Isaiah':
        tMyBookAbbr = 'ISA'
    elif tWEBName == 'James':
        tMyBookAbbr = 'JAM'
    elif tWEBName == 'Jeremiah':
        tMyBookAbbr = 'JER'
    elif tWEBName == 'Job':
        tMyBookAbbr = 'JOB'
    elif tWEBName == 'Joel':
        tMyBookAbbr = 'JOE'
    elif tWEBName == 'John':
        tMyBookAbbr = 'JOH'
    elif tWEBName == 'Jonah':
        tMyBookAbbr = 'JON'
    elif tWEBName == 'Joshua':
        tMyBookAbbr = 'JOS'
    elif tWEBName == 'Jude':
        tMyBookAbbr = 'JDE'
    elif tWEBName == 'Judges':
        tMyBookAbbr = 'JDG'
    elif tWEBName == 'Lamentations':
        tMyBookAbbr = 'LAM'
    elif tWEBName == 'Leviticus':
        tMyBookAbbr = 'LEV'
    elif tWEBName == 'Luke':
        tMyBookAbbr = 'LUK'
    elif tWEBName == 'Malachi':
        tMyBookAbbr = 'MAL'
    elif tWEBName == 'Mark':
        tMyBookAbbr = 'MAR'
    elif tWEBName == 'Matthew':
        tMyBookAbbr = 'MAT'
    elif tWEBName == 'Micah':
        tMyBookAbbr = 'MIC'
    elif tWEBName == 'Nahum':
        tMyBookAbbr = 'NAH'
    elif tWEBName == 'Nehemiah':
        tMyBookAbbr = 'NEH'
    elif tWEBName == 'Numbers':
        tMyBookAbbr = 'NUM'
    elif tWEBName == 'Obadiah':
        tMyBookAbbr = 'OBA'
    elif tWEBName == 'Philemon':
        tMyBookAbbr = 'PHM'
    elif tWEBName == 'Philippians':
        tMyBookAbbr = 'PHP'
    elif tWEBName == 'Proverbs':
        tMyBookAbbr = 'PRO'
    elif tWEBName == 'Psalms':
        tMyBookAbbr = 'PSA'
    elif tWEBName == 'Revelation':
        tMyBookAbbr = 'REV'
    elif tWEBName == 'Romans':
        tMyBookAbbr = 'ROM'
    elif tWEBName == 'Ruth':
        tMyBookAbbr = 'RUT'
    elif tWEBName == 'SongOfSongs':
        tMyBookAbbr = 'SON'
    elif tWEBName == 'Titus':
        tMyBookAbbr = 'TIT'
    elif tWEBName == 'Zechariah':
        tMyBookAbbr = 'ZEC'
    elif tWEBName == 'Zephaniah':
        tMyBookAbbr = 'ZEP'
    return tMyBookAbbr

def notApocrypha(tBook):
    tApocrypha = '|TOB|JDT|ESG|WIS|SIR|BAR|1MA|2MA|1ES|MAN|PS2|3MA|2ES|4MA|DAG|'
    return not(tApocrypha.find(tBook) > 0)


def doHeader(fw2):
    fw2.write('SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";\n')
    fw2.write('START TRANSACTION;\n')
    fw2.write('SET time_zone = "+00:00";\n')
    fw2.write('\n')
    fw2.write('\n')
    fw2.write('/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;\n')
    fw2.write('/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;\n')
    fw2.write('/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;\n')
    fw2.write('/*!40101 SET NAMES utf8mb4 */;\n')
    fw2.write('\n')
    fw2.write('DROP TABLE IF EXISTS `verses`;\n')
    fw2.write('CREATE TABLE `verses` (\n')
    fw2.write('  `verseID` int(11) NOT NULL AUTO_INCREMENT,\n')
    fw2.write('  `bookCode` varchar(3) NOT NULL,\n')
    fw2.write('  `chapter` smallint(4) NOT NULL,\n')
    fw2.write('  `verseNumber` smallint(4) NOT NULL,\n')
    fw2.write('  `verseText` text NOT NULL\n')
    fw2.write('  PRIMARY KEY (`verseID`)\n')
    fw2.write('  UNIQUE KEY `book-chapter-verse` (`bookCode`,`chapter`,`verseNumber`)\n')
    fw2.write(') ENGINE=MyISAM DEFAULT CHARSET=latin1;\n')
    fw2.write('\n')

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

def writeLine(fw, tBook, tChapter, tVerseNum, tVerseText):
    fw.write('INSERT INTO `verses` (`bookCode`, `chapter`, `verseNumber`, `verseText`) VALUES ')
    fw.write('(\'' + tBook + '\',' + tChapter + ',' + tVerseNum + ', \'' + tVerseText.strip() + '\');\n')

def get_line(fr2, bGetStrongsFromFile):
    t_line = fr2.readline()
    t_line = handleStrongs(t_line, bGetStrongsFromFile)
    return t_line

def handleStrongs(t_line, bAddNumbers):
    tWordStart1 = '\\w '
    tWordStart2 = '\\+w '
    tWordEnd1 = '\\w*'
    tWordEnd2 = '\\+w*'
    t_line = handleStrongs2(t_line, bAddNumbers, tWordStart1, tWordEnd1)
    t_line = handleStrongs2(t_line, bAddNumbers, tWordStart2, tWordEnd2)
    return t_line

def handleStrongs2(t_line, bAddNumbers, tWordStart, tWordEnd):
    atStrongs = [
                 'H0113',
                 'H0136',
                 'H0403',
                 'H0410',
                 'H0426',
                 'H0430',
                 'H0433',
                 'H1166',
                 'H1167',
                 'H1376',
                 'H1814',
                 'H2657',
                 'H3050',
                 'H3068',
                 'H4756',
                 'H4886',
                 'H4899',
                 'H5633',
                 'H6212',
                 'H7291',
                 #'H7307',
                 'H7706',
                 'H8314',
                 'G0025',
                 'G0026',
                 'G0027',
                 'G0862',
                 'G1203',
                 'G1459',
                 'G2209',
                 'G2315',
                 'G2519',
                 'G2634',
                 'G2960',
                 'G2961',
                 'G2962',
                 'G3323',
                 'G3841',
                 'G4550',
                 'G4657',
                 'G4995',
                 'G5349',
                 'G5509',
                 'G5546',
                 'G5547',
                 'G5580'
                ]
    t_left = ''
    tWord = ''
    t_right = ''
    while tWordStart in t_line:
        iStrong = 0
        t_left = t_line[0:t_line.find(tWordStart)]
        tStrongs = t_line[t_line.find(tWordStart)+3:t_line.find(tWordEnd):]
        iStrong = tStrongs.find('|strong=')
        tWord = tStrongs[0:iStrong]
        tStrongs = tStrongs[iStrong:]
        tStrongs = tStrongs[9:-1]
        tStrongs = tStrongs[0] + tStrongs[1:].zfill(4)
        if tStrongs in atStrongs and bAddNumbers:
            tStrongs = '{' + tStrongs + '}'
        else:
            tStrongs = ''
        # t_right = t_line[t_line.find(tWordEnd)+3:]
        t_right = t_line[t_line.find(tWordEnd)+len(tWordEnd):]
        t_line = t_left + tWord + tStrongs + t_right
    return t_line

def writeFileName(tFile1):
    tWriteName = ''
    tWriteName = tWriteName + os.path.basename(tFile1)[:-4]
    tWriteName = tWriteName + 'NS'
    tWriteName = tWriteName + '.sql'
    return tWriteName

def stripStrongs(t_line):
    t_strong_start = '{'
    t_strong_end = '}'
    t_left = ''
    t_right = ''
    t_dot = '.'
    while t_strong_start in t_line:
        t_left = t_line[0:t_line.find(t_strong_start)]
        t_right = t_line[t_line.find(t_strong_end) + 1:]
        t_line = t_left + t_right
        t_dot = 's'
    return t_line, t_dot

def strip_strongs_old(t_line):
    t_strong_start = '<'
    t_strong_end = '>'
    t_left = ''
    t_right = ''
    t_dot = '.'
    while t_strong_start in t_line:
        t_left = t_line[0:t_line.find(t_strong_start)]
        t_right = t_line[t_line.find(t_strong_end) + 1:]
        t_line = t_left + t_right
        t_dot = 's'
    return t_line, t_dot

def strip_quotes(t_string):
    return t_string.replace('\\\"', '').replace('\\\'', '') # strips every \" and \' - too many!
    # return t_string.replace('\\\"\\\'', '').replace('\\\"', '') # strips every \"\' and \" - just right?
