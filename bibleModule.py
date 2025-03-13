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
                 'H0113', # 'adon', 'lord', 'Adon - lord or master as opposed to Adonai - MyLord
                 'H0136', # 'Adonai', 'MyLord', 'Adonai - My Lord\r\n\r\nmy Lord\r\nAn emphatic form of \'adon{H0113}\'; the Lord (used as a proper name of God only) -- (my) Lord.\r\n\r\nsee HEBREW \'adon{113}\'
                 'H0403', # 'aken', 'surely', 'Surely, truly, sometimes emphasising a contrast: however
                 'H0410', # 'El', 'God', 'Singular God as opposed to the plural Elohim{H0430}
                 'H0426', # 'Elah', 'God', 'Elah - singular of Elohim{H0430} God or god
                 'H0430', # 'Elohim', 'God', 'Elohim - the plural of eloah, literally \'gods\' often used for the true God
                 'H0433', # 'Eloah', 'God', 'Eloah - the singular of elohim{H430}, literally \'god\'.
                 'H1166', # 'baal', 'Marry/Own', 'Marry/Own
                 'H1167', # 'baal', 'Husband/Master/Owner', 'Husband/Master/Owner
                 'H1376', # 'gevir', 'ruler', 'ruler, master. Not especially interesting perhaps in itself; were it not for the fact it is only used twice - in the story of Jacob as opposed to his brother, Esau - never of God or anyone else.
                 'H1814', # 'dalaq', 'hotly-pursue', 'Hotly-pursue, burn, ignite, inflame
                 'H2657', # 'Hepzibah', 'MyDelightIsInHer', 'Hepzibah = \"my delight is in her\"\r\n1) the queen of King Hezekiah and mother of Manasseh\r\n2) a name for Jesusalem (fig.)
                 'H3050', # 'Yah', 'EverOne', 'Yah - An abbreviation of the proper name for God, Yahweh{H3068}
                 'H3068', # 'Yahweh', 'ForeverOne', 'Yud-Heh-Vav-Heh (Yahweh) - The proper name for God. In Jewish circles never spoken; normally spoken as Adonai ({H136})
                 'H4756', # 'mare', 'lord', 'Master;lord. Only occurs in Daniel
                 'H4886', # 'mashach', 'anoint', 'to anoint (with oil)
                 'H4899', # 'mashiach', 'anointed', 'anointed (Messiah) 
                 'H5633', # 'ceren', 'Lord;tyrant', 'Lord/Tyrant
                 'H6212', # 'esev', 'plant', 'plant, vegetation
                 'H7291', # 'radaph', 'pursue', 'Pursue, follow closely, chase
                 'H7307', # 'ruach', 'spirit/breath/breeze', 'ruach - wind, breath, spirit.
                 'H7706', # 'Shaddai', 'Almighty', 'Almighty - usually God almighty.
                 'H8314', # 'seraphim', 'burningones', 'Fiery; Burning; burningones
                 'H8392', # 'tevah', 'vessel', 'The ark - the vessel which Noah built; the basket vessel in which Moses was placed.
                 'G0025', # 'agapeo', 'Will-Love', 'Determined, active loving that has more to do with willing good for others than any emotional feeling. The verb of {G0026}
                 'G0026', # 'agape', 'Will-Love', 'The determined active love that has more to do with willing good for others than any emotional feeling. The noun of {G0025}
                 'G0027', # 'agapetos', 'dear, dear-ones', 'Beloved, recipients of the greatest love{G0026}, loved
                 'G0444', # 'anthropos', 'people', 'Often translated \'men\' but is not gender specific - so humans, people, humankind.
                 'G0862', # 'afthartos', 'permanent', 'Un-temporary; imperishable; imortal; permanent
                 'G1203', # 'Despotes', 'Master', 'Master - the English \'despot\' comes from this word.
                 'G1459', # 'Enkataleipo', 'Abandon', 'Abandon or Forsake 
                 'G2209', # 'zemia', 'damage', '\'damage/loss\' loss, damage
                 'G2315', # 'Theopneustos', 'Godbreathed', 'Literally the breath/wind/spirit-making of God. God breathed as one word. Only occurs once in 2 Timothy 3:16
                 'G2519', # 'kathegetes', 'teacher', 'teacher
                 'G2634', # 'katakurieuo', 'master', 'master - \'against-lord\'
                 'G2823', # 'klibanos', 'fire-oven', 'This was an earthenware pot for baking bread. It was broader at the bottom than at the top, and with a fire lit inside, the dough was baked by being spread on the outside.
                 'G2960', # 'Kuriakos', 'Master', 'Pertaining to the Lord
                 'G2961', # 'kurieuo', 'dominate', 'master, lord, dominate
                 'G2962', # 'Kurios', 'Lord', 'Lord. Notably this may stand for Yahweh{H3068} as the Jewish tradition to never say Yahweh{H3068}, and say Adonai{H0136} (Lord) instead, was in place long before the New Testament (about 300 BC)
                 'G3107', # 'makarios', 'happier', 'Often translated Blessed, a bit old fashioned now, it is an emphatic form of happy.
                 'G3126', # 'mammon', 'your-savings', 'TrustTreasure - what you rely on, your-savings, investment.
                 'G3323', # 'Messias', 'Messiah', 'Greek transliteration of the Hebrew {H4899}, Mashiach, Messiah. Anointed; Messiah (in Jewish tradition not THE messiah). Only found in John 1 and 4. Equivalent to {G5547}
                 'G3339', # 'metamorfoo', 'transformed', 'This is the Greek root word for the English word Metamorphose.
                 'G3841', # 'Pantokrator', 'Almighty', 'Almighty - only applied (obviously!) to God. Equivalent to {H7706}
                 'G4550', # 'sapros', 'rotten', 'This has a strongly negative meaning- not just rotten but corrupting or causing disease or being diseased.
                 'G4657', # 'skubalon', 'filth', 'Disgusting rubbish; rotten; filth; refuse; dung. This can refer to any of a number of rotten, decaying things that must be disposed of. It is only used in Philippians 3:8.
                 'G4995', # 'sofronismos', 'soundness-of-mind', 'This is subtle and can mean soundness-of-mind, self-discipline, prudence, wisdom. It is only used in 2 timothy 1:7.
                 'G5349', # 'fthartos', 'temporary', 'Temporary or mortal; not lasting, perishable, impermanent.
                 'G5509', # 'chiton', 'tunic', 'Strictly a tunic but often the main or only garment worn, either by men or women. Robe; clothing; undergarment.
                 'G5546', # 'kristianos', 'christian', 'Christian; \'one belonging to Christ\'; Messianic believer;
                 'G5547', # 'Kristos', 'AnointedOne', 'AnointedOne; Christ, anointed one, Messiah
                 'G5580'  # 'pseudokristos', 'pretend-anointed-ones', 'Christ and Messiah both mean anointed one. Ungodly imitators of Jesus Christ will come who make bold claims but are not Him.
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
