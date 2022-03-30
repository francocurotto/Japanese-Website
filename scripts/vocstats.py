import os

vocdir = "../content/vocabulary/"
filelist = os.listdir(vocdir)
# ommited lists
filelist.remove("_index.md")
filelist.remove("hiragana.md")
filelist.remove("honorifics.md")
filelist.remove("katakana.md")
filelist.remove("particles.md")

# data variables
english = set()
kana = set()
kanji = set()

def main():
    for filename in filelist:
        with open(vocdir+filename) as vocfile:
            process_file(vocfile)
    print("English entries:" + str(len(english)))
    print("Kana entries:" + str(len(kana)))
    print("Kanji entries:" + str(len(kanji)))

def process_file(vocfile):
    table_starts = False
    for line in vocfile:
        if line.startswith("|-"):
            table_starts = True
        elif line.strip() == "":
            table_starts = False
        elif table_starts:
            process_line(line)

def process_line(line):
    voclist = line.split("|") # split line into entry list

    # differencite between table with and without icon
    if len(voclist) == 4:
        voclist = voclist[1:3]
    elif len(voclist) == 5:
        voclist = voclist[1:4]
    elif len(voclist) == 6:
        voclist = voclist[2:5]
    else: # should not happen
        print(voclist)

    # add to sets
    english.update([voclist[0].strip()])
    kana.update([voclist[1].strip()])
    if len(voclist) == 3:
        kanji.update([voclist[2].strip()])

if __name__ == "__main__":
    main()
