from sty import fg, bg, ef, rs
import random




racecol   ={"human":(159),
            "elf":(154),
            "orc":(174),
            "undead":(135),
            "ent":(173),
            "goblin":(220),
            "wolfy":(4)
            }

Life     = 114
Mana     = 38
Talent   = 141
Item     = 145
OKGreen  = (10)
Danger   = (9)
Critical = (166)
Gold     = (220)
XP       = 173
SQuest    = 219

def add_color(msg,fore):
    if type(msg) != str:
        msg=str(msg)
    mat=fg(fore) + msg + fg.rs
    return (mat)

def add_bold(msg):
    if type(msg) != str:
        msg=str(msg)
    mat=ef.bold + msg + rs.bold_dim
    return (mat)

def givemeans(n,s):
    if n>1:
        return str(n)+" "+s+"s"
    return str(n)+" "+s

def ans(n):
    if n>1:
        return "s"
    return ""

def seqspider():
    s="/╲/\\╭(•‿•)╮/\\╱\\"
    return add_color(s,random.randint(124,231))

def padleft(s,n=3):
    if type(s)!= str:
        s=str(s)
    a = max(0,n-len(s))
    return " "*a +s

def center(s,n=80):
    L=n-len(s)
    return " "*(L//2)+s

def box_strings(t,t2):  # Assume n lines to be diplayed on 2n+1, t is the colorless version cause...
    # find max length:
    m=0
    for x in t:
        if len(x) > m :
            m = len(x)
    m=m+2
    l=["*"*(m+2)]
    for i in range(0,len(t)):
        if i >0:
            l.append("*"+" "*m+"*")
        s = m-len(t[i])
        b = i%2
        l.append("*"+" "*((s+b)//2)+t2[i]+" "*((s+1-b)//2)+"*")
    l.append("*"*(m+2))
    return l

def invalid_ans():
    s="\t 🔥 This is not a valid answer. "
    lsilly=["Please remove the arrow from your ear and try again.",
    "I guess some nasty gremlin ran on your keyboard.",
    "Sometimes, you can blame your cat, but maybe not today.",
    "Are you trying to list the error messages?",
    "Try to type do do do do, try to type do do do do, try to type.",
    "Take a deep breath, and try again.",
    "What is yellow, and equivalent to the axiom of Choice? Zorn's lemma!"]
    s+=random.choice(lsilly)+" 🔥"
    print(s)
