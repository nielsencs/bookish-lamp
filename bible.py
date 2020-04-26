import os

path = 'E:\\GitHub\\bookish-lamp\\eng-web_usfm'
chapter = 0
para = ''
comStart = '\\f'
comEnd = '\\f*'

os.chdir(path)
for filename in os.listdir(path):
    if filename.endswith('.usfm'):
        print('processing ' + filename, end='')
        fr = open(filename, 'r', encoding="utf8")
        fw = open(filename + '.txt', 'w', encoding="utf8")
        line = fr.readline()
        while line:
            if line.startswith('\\c'):
                chapter = line[3:-1]
            if line.startswith('\\p'):
                para = line[3:-1]
            else:
                para = ''
            if line.startswith('\\v'):
                if comStart in line:
                    line=line[0:line.find(comStart)] + line[line.find(comEnd)+3:]
                    print('+', end='')
                else:
                    print('-', end='')
                fw.write(chapter + line[3:] + para)
            else:
                print('.', end='')
            line = fr.readline()
            
        fr.close()
        fw.close()
        print('')
