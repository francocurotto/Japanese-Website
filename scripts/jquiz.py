from urwid import *

# basic elements
div = Divider()
tltbanner = Text("Translate to Kanji:", align="center")
tltitem = Text("souvenir", align="center")
ansbanner = Text("Answer:", align="center")
ansitem = Text("お土産", align="center")
hintbanner = Text("Hints:", align="center")
hintitem = Text("お土", align="center")
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
itemlist = [div, tltbanner, tltitem, div, ansbanner, ansitem, 
   div, hintbanner, hintitem, div, infocol1, infocol2, infocol3]
pile = Pile(itemlist)
linebox = LineBox(pile, "JQuiz")
filler = Filler(linebox, valign="top")
loop = MainLoop(filler)
loop.run()
