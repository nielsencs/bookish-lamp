import tkinter as tk
from tkinter import filedialog

from bibleModule import writeFileName, stripStrongs, strip_strongs_old, strip_quotes

oRoot = tk.Tk()
oRoot.withdraw()

#globals
tPath1 = 'generatedSQL'

def main():
    tFile1 = filedialog.askopenfilename(initialdir = tPath1,
                                       title = 'Select file',
                                       filetypes = (('SeQueL files','*.sql'),('TeXT files','*.txt'),('all files','*.*')))

    print(tFile1)

    tWriteName = writeFileName(tFile1)
    fw = open(tPath1 + '\\' + tWriteName, 'w', encoding="utf8")

    fr1 = open(tFile1, 'r', encoding="utf8")
    t_line_1 = fr1.readline()

    while t_line_1:
        t_line_1, tDot = stripStrongs(t_line_1)
        t_line_1, tDot = strip_strongs_old(t_line_1)
        t_line_1 = strip_quotes(t_line_1)
        
        print(tDot, end='')
        fw.write(t_line_1)
        t_line_1 = fr1.readline()

    fr1.close()
    fw.close()

main()
