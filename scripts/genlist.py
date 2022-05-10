import os

vocdir = "../content/vocabulary/"
filelist = os.listdir(vocdir)
filelist

def genlist():
    tablelist = get_tables()
    voclist = get_voclist(tablelist)
    return voclist

def get_tables():
    tablelist = [[]]
    for filename in filelist:
        with open(vocdir+filename, "r") as vocfile:
            for line in vocfile:
                # if not in table and last table not empty
                if not line.startswith("|") and tablelist[-1]:
                    tablelist.append([]) # start new table
                elif line.startswith("|"): # if in table
                    # add line to last table
                    tablelist[-1].append(line)
    # remove non-table files like _index.md
    tablelist = [t for t in tablelist if t != []]

    return tablelist

def get_voclist(tablelist):
    voclist = []
    for table in tablelist:
        # read first line
        keys = get_words(table[0])
        # skip line with not english or kana
        if not "English" in keys or not "Kana" in  keys:
            continue
        # add voc items to list
        for line in table[2:]:
            words = get_words(line)
            voclist.append(dict(zip(keys, words)))
    return voclist

def get_words(line):
    return [w.strip() for w in line.split("|")][1:-1]

if __name__ == "__main__":
    genlist()
