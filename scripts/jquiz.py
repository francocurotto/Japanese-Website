from argparse import ArgumentParser, ArgumentTypeError
from random import sample
from urwid import *
from genlist import genlist

global tltlang, anslang, nitems, ntries, quizdict, totscore
global tltitem, ansitem, hintitem
global triesinfo, itemsinfo, scoreinfo
global ntry, score
score = 0
totscore = 10

def main():
    global quizdict, nitems
    args = get_cmd_args()
    quizdict = gen_dict()
    nitems = get_nitems(args.nitems)
    quizdict = shuffle_dict()
    loop = init_interface(args, quizdict)
    loop.run()

def get_cmd_args():
    global tltlang, anslang, ntries
    parser = ArgumentParser(description="Train Japanese " +
        "by translating items from the website vocabulary.")
    parser.add_argument("-l", "--language-translate", 
        choices=["english", "japanese"], default="english",
        dest="tltlang", help="Language to translate.")
    parser.add_argument("-j", "--japanese-syllabary", 
        choices=["kana", "kanji"], default="kana",     
        dest="syllab", help="Use japanese in kana or kanji.")
    parser.add_argument("-i", "--items", default=0, type=int,
        dest="nitems", help="Number of items in the quiz." +
            "Use <=0 for all items in vocabulary.")
    parser.add_argument("-t", "--tries", default=0, type=int,
        dest="ntries", help="Number if tries for each item " +
            "in quiz. Use <=0 for unlimites tries.")
    args = parser.parse_args()
    tltlang, anslang = get_langs(args.tltlang, args.syllab)
    ntries = args.ntries
    return args

def get_langs(tltlang, syllab):
    if tltlang == "japanese":
        return syllab.capitalize(), "English"
    return "English", syllab.capitalize()

def gen_dict():
    itemlist = genlist()
    quizdict = {}
    for item in itemlist:
        if tltlang in item and anslang in item:
            if not item[tltlang] in quizdict:
                quizdict[item[tltlang]] = [item[anslang]]
            else:
                quizdict[item[tltlang]].append(item[anslang])
    return quizdict

def get_nitems(nitems):
    if nitems <= 0 or len(quizdict) < nitems:
        return len(quizdict)
    return nitems

def shuffle_dict():
    global quizdict
    keys = sample(list(quizdict), nitems)
    quizdict = {key: quizdict[key] for key in keys}
    return quizdict

def init_interface(args, quizdict):
    global tltitem, ansitem, hintitem
    global triesinfo, itemsinfo, scoreinfo
    # quiz elements
    div = Divider()
    tltbanner = Text("Translate to " + anslang + ":",
        align="center")
    tltitem = Text("", align="center")
    #ansbanner = Text("Answer:", align="center")
    #ansitem = Text("", align="center")
    ansitem = Edit(u"Answer:\n", align="center")
    hintbanner = Text("Hints:", align="center")
    hintitem = Text("", align="center")
    
    # info elements
    hintctrl = Text("CTRL+h:hint")
    triesbanner = Text("tries:", align="right")
    triesinfo = Text("", align="right")
    infocol1 = Columns([hintctrl, triesbanner,(8, triesinfo)])
    nextctrl = Text("CTRL+n:next")
    itemsbanner = Text("items:", align="right")
    itemsinfo = Text("", align="right")
    infocol2 = Columns([nextctrl, itemsbanner, (8, itemsinfo)])
    quitctrl = Text("CTRL+q:quit")
    scorebanner = Text("score:", align="right")
    scoreinfo = Text("", align="right")
    infocol3 = Columns([quitctrl, scorebanner, (8, scoreinfo)])
    set_newitem()

    # main elements
    itemlist = [div, tltbanner, tltitem, div, ansitem, div,
        hintbanner, hintitem, div, infocol1, infocol2, infocol3]
    pile = Pile(itemlist)
    linebox = LineBox(pile, "JQuiz")
    filler = Filler(linebox, valign="top")
    loop = MainLoop(filler)
    return loop

def set_newitem():
    # get the new item
    global quizdict, tltitem, ntry
    item = quizdict.popitem()
    tltitem.set_text(item[0])
    ntry = 1; set_triesinfo()
    set_itemsinfo()
    set_scoreinfo()

def set_triesinfo():
    triesinfo.set_text(str(ntry) + "/" + str(ntries))

def set_itemsinfo():
    nitem = nitems - len(quizdict)
    itemsinfo.set_text(str(nitem) + "/" + str(nitems))

def set_scoreinfo():
    scoreinfo.set_text(str(score) + "/" + str(totscore))


if __name__ == "__main__":
    main()
