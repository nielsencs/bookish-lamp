from bibleModule import writeFileName, stripStrongs, strip_quotes
import PySimpleGUI as sg

# globals
tPath1 = 'generatedSQL'

def swap_dont(t_string):
    return t_string.replace('Don\\\'t', 'You shall not')

def swap_mustnt(t_string):
    return t_string.replace('mustn\\\'t', 'shall not')

def swap_booths(t_string):
    return t_string.replace('temporary-shelters', 'temporary shelters')

def swap_enter(t_string):
    return t_string.replace('enter', 'come into')

def swap_lords(t_string):
    return t_string.replace('LordOfMine{H0136}', 'Lord{H0136}')

def swap_chase(t_string):
    return t_string.replace('pursue', 'chase')

def swap_group(t_string):
    return t_string.replace('group', 'company')

def swap_murmur(t_string):
    return t_string.replace('murmur', 'complain')

def swap_testimony(t_string):
    return t_string.replace('testimony', 'covenant')

def swap_winepress(t_string):
    return t_string.replace('winepress', 'wine press')

def swap_throw(t_string):
    return t_string.replace('throw', 'cast')

def strip_paras_plus(t_string):
    return t_string.replace('<p>', '').replace('</p>', '').replace('<br>', '')

def strip_squares(t_string):
    t_string = t_string.replace('[', '')
    return t_string.replace(']', '')


def process_line(t_line):
    t_line = swap_dont(t_line)
    t_line = swap_mustnt(t_line)
    t_line = swap_lords(t_line)
    t_line = swap_booths(t_line)
    t_line = swap_enter(t_line)
    t_line = swap_chase(t_line)
    t_line = swap_group(t_line)
    t_line = swap_murmur(t_line)
    t_line = swap_testimony(t_line)
    t_line = swap_winepress(t_line)
    t_line = swap_throw(t_line)

    t_line = strip_paras_plus(t_line)
    t_line = strip_quotes(t_line)
    t_line = strip_squares(t_line)

    t_line, t_dot = stripStrongs(t_line)
    return t_line, t_dot

def write_bible_verses():
    t_file_1 = 'D:/Python/bookish-lamp/database/bibleVerses.sql'
    t_write_name_1 = writeFileName(t_file_1)

    try:
        with open(t_file_1, 'r', encoding="utf8") as fr1, open(tPath1 + '\\' + t_write_name_1, 'w', encoding="utf8") as fw:
            for t_line_1 in fr1:
                t_line_1, t_dot = process_line(t_line_1)
                print(t_dot, end='')
                fw.write(t_line_1)
    except IOError as e:
        print(f"An error occurred: {e}")

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

def get_name(text):
    return text.replace(" ", "").replace(":", "_").strip()

gui()