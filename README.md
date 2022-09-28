# bookish-lamp
Some basic tools to edit my bible, based on the WEB public domain Bible.

This is VERY MUCH a WiP! The purpose is to prepare a full (without apocrypha) Bible text for my website BibleStudyMan.co.uk. I've opted (so far) to use the downloadable WEB USFM format files as my source. Then I convert them to SQL and modify as I learn and get inspiration for changes to modernise some passages and more closely match the original text.
The following is some explanation of what the files are intented for:

Any folder starting 'eng-web-usfm' is a WEB download taken from https://ebible.org/find/details.php?id=eng-web&all=1 with date: eng-web-usfm_yyyy-mm-dd e.g. eng-web-usfm_2021-02-14 was from 14th February 2021
eng-asv_usfm_2022-08-01              -    Like the WEB downloads, but the ASV on which the WEB is based https://ebible.org/find/details.php?id=eng-asv
engasvbt_usfm_2022-02-09             -    Like the WEB downloads, but the Byzantine Text ASV https://ebible.org/find/details.php?id=engasvbt
WEB(2011)                            -    The original Bible text files I got of the WEB in 2012

bibleFromWEB(2011).py                -    Converts the WEB(2011) to SQL
bibleFromUSFM.py                     -    Converts the USFM to SQL
bibleFromUSFM_strongs.py             -    in September 2119 the USFM files began to have strongs numbers added
bibleModule.py                       -    routines used by the above scripts
generatedSQL                         -    repository of converted files

compare2filesNew.py                  -    used to produce text file showing lines that differ between versions
comparisons                          -    Repository of version comparisons e.g:
|_WEB(2011)bible-vs-bibleVerses.sql  -    comparison of original 2011 text and my latest (including many but not all WEB changes)
database                             -    where 'final' Bible database resides
|_bibleVerses.sql                    -    the master SQL Bible used in my website

BibleTemplate.txt                    -    Blank Bible verses
Psalm119Letters.txt                  -    List of the Hebrew letters in Psalm 119

compareWEB.py                        -    compare eng-web-usfm editions to see what they've been up to!
WEBChanges.txt                       -    Output of compareWEB.py

combineTwoVersions.py                -    WiP - these are my fumbling attempts to compare, select, and edit different bible versions/editions
combineVersions.py                   -    WiP

Ignore the following (yes I know if I was doing this 'properly' they wouldn't be here at all!):
stripStrongs.py                      -    
versesMaster_1.txt                   -    
versesMaster_2.txt                   -    
