from bibleModule import writeFileName, stripStrongs
import PySimpleGUI as sg
#globals
tPath1 = 'generatedSQL'

def stripParas(tString):
    return tString.replace('<p>', '').replace('</p>', '')

def stripQuotes(tString):
    return tString.replace('\\\"\\\'', '')

def swapLords(tString):
    return tString.replace('LordOfMine{H0136}', 'Lord{H0136}')

def writeBibleVerses():
    tFile1 = 'D:/Python/bookish-lamp/database/bibleVerses.sql'

    tWriteName = writeFileName(tFile1)
    fw = open(tPath1 + '\\' + tWriteName, 'w', encoding="utf8")

    fr1 = open(tFile1, 'r', encoding="utf8")
    tLine1 = fr1.readline()

    while tLine1:
        tLine1 = stripParas(tLine1)
        tLine1 = stripQuotes(tLine1)
        tLine1 = swapLords(tLine1)
        
        tLine1, tDot = stripStrongs(tLine1)
        print(tDot, end='')
        fw.write(tLine1)
        tLine1 = fr1.readline()

    fr1.close()
    fw.close()

def gui():
    sg.theme('Dark Blue 3')
    app_name = 'stripStrongs_bibleVerses_GUI.py'

    layout = [
                [sg.Button('Cut bibleVerses Strong\'s', key='bGO')],
            ]

    window = sg.Window(app_name, layout)
    b_do_it = True
    while b_do_it:
        event, _ = window.read()
        if event:
            if event == 'bGO':
                writeBibleVerses()
        else:
            b_do_it = False


def get_name (text):
    return text.replace(" ", "").replace(":", "_").strip()

gui()
