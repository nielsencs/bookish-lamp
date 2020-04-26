import os

def main():
    tPath1 = 'E:\\GitHub\\bookish-lamp\\structure'
    tPath2 = 'E:\\GitHub\\bookish-lamp\\eng-web_usfm'
    tChapter = ''
    tVerse = ''
    para = ''
    comStart = '\\f'
    comEnd = '\\f*'

    os.chdir(tPath1)
    fr1 = open('versesMaster.sql', 'r')
    os.chdir(tPath2)
    fw = open('..\\versesMaster.usfm.txt', 'w', encoding="utf8")
    for filename in os.listdir(tPath2):
        if filename.endswith('.usfm'):
            tBook = filename[3:6]
            print('processing ' + filename, end='')
            fr2 = open(filename, 'r', encoding="utf8")
            line1 = findVerse(fr1,"'")
            line2 = fr2.readline()
            while line2:
                if line2.startswith('\\c'):
                    tChapter = line2[3:-1]
                if line2.startswith('\\p'):
                    para = line2[3:-1]
                else:
                    para = ''
                if line2.startswith('\\v'):
                    tVerse = line2[2:5]
                    if comStart in line2:
                        line2=line2[0:line2.find(comStart)] + line2[line2.find(comEnd)+3:]
                        print('+', end='')
                    else:
                        print('-', end='')
                    line2 = swapQuotes(firstAlpha(line2[3:] + para))
                    line2=line2.rstrip()
                    if line1 != line2:
                        #print(line1)
                        fw.write(tBook + tChapter + tVerse + ':' + line1 + '\n')
                        fw.write(tBook + tChapter + tVerse + ':' + line2 + '\n')
                    #else:
                        
                    line1 = findVerse(fr1,"'")
                else:
                    print('.', end='')
                line2 = fr2.readline()
                #line2 = ''
            fr2.close()
            print('')
    fr1.close()
    fw.close()

def firstAlpha(line):
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

def findVerse(fr, tVerse):
    line = fr.readline()
    bDoIt = True
    while bDoIt:
        if tVerse in line:
            bDoIt = False
            line = line[10:]
            line = line[line.find(tVerse)+1:-4]
            #print('')
            #print(line)
            #line = line[0:line.find(tVerse)]
            #print(line)
            line = trimAngleBrackets(line)
            #print(line)
            line = trimChar(line, '\\')
        else:
            line = fr.readline()
    return line

main() 
