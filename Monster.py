import random

defmon= {"cryptographer" :(3,0,1,3),   "moth"           :(1,1,0,0),
         "butterfly"     :(2,2,0,1),   "bee"            :(3,3,0,2),
         "bear"          :(6,7,0,0),   "mage"           :(10,10,1,4),
         "soldier"       :(10,10,0,5), "wizard"         :(11,12,1,3),
         "ghost broccoli":(12,10,1,4), "ghost pepper"   :(13,12,0,5),
         "slime"         :(14,14,2,6), "icthyocentaur"  :(15,14,0,7),
         "demon"         :(13,12,2,3), "vampire"        :(14,15,1,4),
         "werewolf"      :(15,15,0,7), "elemental"      :(15,15,1,4),
         "moon alien"    :(18,20,2,8), "roussalka"      :(19,20,1,9),
        "space soldier" :(20,25,0,10),"space wizard"   :(21,26,1,10),
        "space demon"   :(21,27,2,12),"crazy cat"      :(25,28,2,10),
         "inugami"       :(26,27,0,13),"naga sorceress" :(27,28,1,15),
         "naga footman"  :(27,27,0,15),"naga overlord"  :(28,28,2,16),
         "void marksman" :(26,30,0,12),"void sorcered"  :(30,34,1,15),
         "void anointed" :(32,35,2,16),"addanc"         :(33,36,0,17),
         "kraken"        :(34,38,0,15),"incubbus"       :(36,37,2,16),
         "cerberus"      :(37,39,0,17),"hydra"          :(37,37,1,18),
         "nian"          :(40,42,2,20),"efrit"          :(40,41,1,16),
         "Rakshasas"     :(41,42,0,18)
         } # Name, base xp, base dmg, phy|mag|chaos, loot
limon = list(defmon.keys())

class Mon:
    def __init__(self,name,c):
        self.name=name
        self.xp=c[0]
        self.dam=c[1]
        self.typ=c[2]
        self.loot=c[3]

def relslice(lvl):
    '''

    Parameters
    ----------
    lvl : int, user level.

    Returns
    -------
    list of appropriate monster names.

    '''

    l = len(limon)
    minslice=min(max(0,lvl-2),l-1)
    maxslice=(min(l, lvl+2))
    return limon[minslice:maxslice]

def pickmonster(lvl):
    '''
    Parameters
    ----------
    lvl : int

    Returns
    -------
    monstrinou : a valid monster for the lvl range

    '''
    name = random.choice(relslice(lvl))
    c = defmon[name]
    monstrinou = Mon(name,c)
    return monstrinou
