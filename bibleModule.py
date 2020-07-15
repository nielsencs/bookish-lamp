def trimComments(tLine):
    comStart = '\\f'
    comEnd = '\\f*'
    com2Start = '\\x'
    com2End = '\\x*'
    if comStart in tLine:
        tLine=trimExtras(tLine, comStart, comEnd)
        #print('+', end='')
    #else:
        #print('-', end='')

    if com2Start in tLine:
        tLine=trimExtras(tLine, com2Start, com2End)
        #print('#', end='')
    #else:
        #print('-', end='')
    return tLine

def trimExtras(line, lDelim, rDelim):
    #bDoIt = True
    while lDelim in line:
        lLine = line[0:line.find(lDelim)]
        rLine = line[line.find(rDelim)+3:]
        line = lLine + rLine
    return line

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
