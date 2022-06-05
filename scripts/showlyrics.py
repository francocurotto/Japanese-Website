import sys
from urwid import *

songdict = {"Japanese":[],"Romaji":[],"English":[]}
palette = [("Japanese", "dark red",   "black"),
           ("Romaji",   "dark green", "black"),
           ("English",  "dark cyan",  "black")]

def main():
    songfile = sys.argv[1] 
    songname = get_songinfo(songfile)
    loop = init_interface(songname)
    loop.run()

def get_songinfo(songfile):
    filelines = get_filelines(songfile)
    songname = get_songname(filelines[1])
    fill_songdict(filelines)
    return songname

def get_filelines(filename):
    with open(filename) as f: 
        filelines = f.readlines()
    return filelines

def get_songname(nameline):
    init = nameline.index('"')
    end = nameline.index('"', init+1)
    return nameline[init+1:end]

def fill_songdict(filelines):
    for line in filelines:
        if is_songline(line):
            add2dict(line)

def is_songline(line):
    is_table = line.startswith("| ")
    is_head  = line.startswith("| J")
    return is_table and not is_head

def add2dict(line):
    songlines = get_songlines(line)
    songdict["Japanese"].append(songlines[0])
    songdict["Romaji"]  .append(songlines[1])
    songdict["English"] .append(songlines[2])

def get_songlines(line):
    return [l.strip() for l in line.split("|")][1:-1]

def init_interface(songname):
    walker = create_walker()
    listbox = MyListBox(walker)
    linebox = LineBox(listbox, " " + songname + " ")
    loop = MainLoop(linebox,palette,unhandled_input=exit_loop)
    return loop

def create_walker():
    jlines = songdict["Japanese"]
    rlines = songdict["Romaji"]
    elines = songdict["English"]
    content = [Divider()]
    for jline, rline, eline in zip(jlines, rlines, elines):
        if jline:
            jtext = Text(("Japanese", jline), align="center")
            rtext = Text(("Romaji",   rline), align="center")
            etext = Text(("English",  eline), align="center")
            div = Divider()
            content += [jtext, rtext, etext, div]
        else:
            content += [Divider(), Divider()]
    return SimpleFocusListWalker(content)
 
def exit_loop(key):
    if key == "esc":
        raise ExitMainLoop()

class MyListBox(ListBox):
    def mouse_event(self,size,event,button,col,row,focus):
        super().mouse_event(size,event,button,col,row,focus)
        if button == 4.0:
            self.keypress(size, "up")
        elif button == 5.0:
            self.keypress(size, "down")

if __name__ == "__main__":
    main()
