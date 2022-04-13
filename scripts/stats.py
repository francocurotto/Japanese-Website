from genlist import genlist

voclist = genlist()
english = set()
kana    = set()
kanji   = set()

for vocitem in voclist:
    english.add(vocitem["English"])
    kana.add(vocitem["Kana"])
    if "Kanji" in vocitem:
        kw = vocitem["Kanji"]
        kl = filter(lambda x: 13312<ord(x)<40879, kw)
        kanji.update(kl)
print("Total number of entries:  " + str(len(voclist)))
print("Distinct English entries: " + str(len(english)))
print("Distinct Kana entries:    " + str(len(kana)))
print("Distinct singular Kanjis: " + str(len(kanji)))
