#open Original WEB
#prepare BSM:
    #open current BSM version
    #remove strongs number tags
#compare BSM with WEB:
    #flag changed lines as BSM
#prepare USFM:
    #open latest usfm folder
    #process into SQL
    #remove strongs number tags
#compare USFM with WEB:
    #flag changed lines as USFM
#if line flagged as USFM AND BSM:
    #present to user for selection/editing
    #store resolution


tPath = 'E:\\GitHub\\bookish-lamp\\'
tFileWEBO = 'generatedSQL\\WEB(2011)bible'         # + '.sql' or + 'NS.sql' 'Original' WEB
tFileWEBC = 'generatedSQL\\USFM_2021-04-01_bible1' # + '.sql' or + 'NS.sql' 'Current'  WEB
tFileBSMC = 'database\\bibleVerses.sql'            # 'Current'  BSM
