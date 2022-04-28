from argparse import ArgumentParser, ArgumentTypeError
from random import sample
from urwid import *
from genlist import genlist

def main():
    args = get_cmd_args()
    quizdict = gen_dict(args.tltlang, args.syllab)
    quizdict = shuffle_dict(quizdict, args.nitems)
    print(quizdict)
    #loop = init_interface()
    #loop.run()

def get_cmd_args():
    parser = ArgumentParser(description="Train Japanese " +
        "by translating items from the website vocabulary.")
    parser.add_argument("-l", "--language-translate", 
        choices=["english", "japanese"], default="english",
        dest="tltlang", help="Language to translate.")
    parser.add_argument("-j", "--japanese-syllabary", 
        choices=["kana", "kanji"], default="kana",     
        dest="syllab", help="Use japanese in kana or kanji.")
    parser.add_argument("-i", "--items", default="full",
        type=check_nitems, dest="nitems",
        help="Number of items in the quiz." +
            "Use 'full' for all items in vocabulary.")
    args = parser.parse_args()
    return args

def check_nitems(string):
    if string == "full": return string
    if nitems := int(string) < 1:
        raise ArgumentTypeError("# of items must be positive.")
    return nitems

def gen_dict(tltlang, syllab):
    itemlist = genlist()
    tltkey, anskey = get_keys(tltlang, syllab)
    quizdict = {}
    for vocitem in itemlist:
        if tltkey in vocitem and anskey in vocitem:
            if not tltkey in quizdict:
                quizdict[tltkey] = [anskey]
            else:
                quizdict[tltkey].append(anskey)
    return quizdict

def get_keys(tltlang, syllab):
    if tltlang == "Japanese":
        return syllab.capitalize(), "English"
    return "English", syllab.capitalize()

def shuffle_dict(quizdict, nitems):
    if nitems == "full" or len(quizdict) < nitems:
        nitems = len(quizdict)
    keys = sample(list(quizdict), nitems)
    quizdict = {key: quizdict[key] for key in keys}
    return quizdict

def init_interface():
    # quiz elements
    div = Divider()
    tltbanner = Text("Translate to Kanji:", align="center")
    tltitem = Text("souvenir", align="center")
    ansbanner = Text("Answer:", align="center")
    ansitem = Text("お土産", align="center")
    hintbanner = Text("Hints:", align="center")
    hintitem = Text("お土", align="center")
    
    # info elements
    hintctrl = Text("CTRL+h:hint")
    triesbanner = Text("tries:", align="right")
    triesinfo = Text("1/.", align="right")
    infocol1 = Columns([hintctrl, triesbanner,(8, triesinfo)])
    nextctrl = Text("CTRL+n:next")
    itemsbanner = Text("items:", align="right")
    itemsinfo = Text("1/10000", align="right")
    infocol2 = Columns([nextctrl, itemsbanner, (8, itemsinfo)])
    quitctrl = Text("CTRL+q:quit")
    scorebanner = Text("score:", align="right")
    scoreinfo = Text("0/0", align="right")
    infocol3 = Columns([quitctrl, scorebanner, (8, scoreinfo)])

    # main elements
    itemlist = [div, tltbanner, tltitem, div, ansbanner,
        ansitem, div, hintbanner, hintitem, div, infocol1,
        infocol2, infocol3]
    pile = Pile(itemlist)
    linebox = LineBox(pile, "JQuiz")
    filler = Filler(linebox, valign="top")
    loop = MainLoop(filler)
    return loop

if __name__ == "__main__":
    main()
