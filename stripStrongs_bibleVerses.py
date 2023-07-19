from bibleModule import writeFileName, stripStrongs

#globals
tPath1 = 'generatedSQL'

def main():
    tFile1 = 'D:/Python/bookish-lamp/database/bibleVerses.sql'

    tWriteName = writeFileName(tFile1)
    fw = open(tPath1 + '\\' + tWriteName, 'w', encoding="utf8")

    fr1 = open(tFile1, 'r', encoding="utf8")
    tLine1 = fr1.readline()

    while tLine1:
        tLine1, tDot = stripStrongs(tLine1)
        print(tDot, end='')
        fw.write(tLine1)
        tLine1 = fr1.readline()

    fr1.close()
    fw.close()

main()
