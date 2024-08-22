from bibleModule import writeFileName, stripStrongs
import PySimpleGUI as sg
#globals
tPath1 = 'generatedSQL'

def strip_paras(t_string):
    return t_string.replace('<p>', '').replace('</p>', '')

def strip_quotes(t_string):
    # return t_string.replace('\\\"', '').replace('\\\'', '') strips every \" and \' - too many!
    return t_string.replace('\\\"\\\'', '').replace('\\\"', '') # strips every \"\' and \" - just right?

def swap_lords(t_string):
    return t_string.replace('LordOfMine{H0136}', 'Lord{H0136}')

def write_bible_verses():
    t_file_1 = 'D:/Python/bookish-lamp/database/bibleVerses.sql'

    t_write_name_1 = writeFileName(t_file_1)
    fw = open(tPath1 + '\\' + t_write_name_1, 'w', encoding="utf8")

    fr1 = open(t_file_1, 'r', encoding="utf8")
    t_line_1 = fr1.readline()

    while t_line_1:
        t_line_1 = strip_paras(t_line_1)
        t_line_1 = strip_quotes(t_line_1)
        t_line_1 = swap_lords(t_line_1)
        
        t_line_1, t_dot = stripStrongs(t_line_1)
        print(t_dot, end='')
        fw.write(t_line_1)
        t_line_1 = fr1.readline()

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
                write_bible_verses()
        else:
            b_do_it = False


def get_name (text):
    return text.replace(" ", "").replace(":", "_").strip()

gui()
