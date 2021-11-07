# -*- coding: utf-8 -*-
"""
Initially done by Olivier Blazy
This does not aim to be anything wonderful
"""

import sys
import random
import time
import pickle
import os

listyes = ["y","Y","O","o","yes","YES","oui","OUI","j","J","ja","JA"]
listno = ["n","N","no","NO","no","NO","nein","NEIN"]

class PrettyUI:

    racecol={"human":(120,120,240),
             "elf":(80,230,80),
             "orc":(200,120,120),
             "undead":(200,10,200),
             "ent":(170,120,120),
             "goblin":(212,175,55),
             "wolfy":(44,191,169)
             }

    OKGreen = (10,255,10)
    Critical= (220,157,51)
    Danger  = (200,30,30)
    Gold    = (212,175,55)

    def add_color(msg,fore):
        rf,gf,bf=fore
        msg='{0}' + str(msg)
        mat='\33[38;2;' + str(rf) +';' + str(gf) + ';' + str(bf)  +'m'
        return (msg .format(mat)+'\33[0m')

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
        return PrettyUI.add_color(s,(random.randint(125,230),random.randint(125,230),random.randint(125,230)))

class Perso:
    defattr={
        "human"     :{"CON":(10,(1,2)), "STR":(10,(1,2)),"INT":(10,(1,2)),"WIS":(10,(1,2)),"DEX":(10,(1,2)),"LUC":(10,(1,2)),"STA":(10,(1,2)),"SPD":(10,(1,1)),"CHA":(10,(1,2)),"PER":(10,(1,2))},
        "undead"    :{"CON":(8,(0,2)), "STR":(11,(2,3)),"INT":(9,(1,1)),"WIS":(12,(0,1)),"DEX":(8,(1,1)),"LUC":(10,(1,2)),"STA":(14,(1,3)),"SPD":(8,(0,1)),"CHA":(10,(1,1)),"PER":(10,(1,2))},
        "elf"       :{"CON":(9,(0,1)), "STR":(8,(1,1)),"INT":(8,(2,3)),"WIS":(13,(3,4)),"DEX":(25,(3,6)),"LUC":(10,(3,4)),"STA":(11,(1,2)),"SPD":(12,(2,2)),"CHA":(11,(1,3)),"PER":(12,(1,3))},
        "orc"       :{"CON":(15,(2,3)), "STR":(10,(3,4)),"INT":(10,(0,1)),"WIS":(10,(0,1)),"DEX":(10,(0,1)),"LUC":(10,(0,1)),"STA":(15,(2,3)),"SPD":(10,(1,2)),"CHA":(10,(2,3)),"PER":(9,(0,2))},
        "ent"       :{"CON":(15,(3,3)), "STR":(10,(2,2)),"INT":(10,(1,2)),"WIS":(10,(0,1)),"DEX":(10,(0,1)),"LUC":(8,(0,1)),"STA":(12,(1,3)),"SPD":(10,(0,1)),"CHA":(12,(2,2)),"PER":(10,(1,1))},
        "goblin"    :{"CON":(15,(3,3)), "STR":(10,(2,2)),"INT":(10,(1,2)),"WIS":(10,(0,1)),"DEX":(10,(0,1)),"LUC":(8,(0,1)),"STA":(12,(1,3)),"SPD":(10,(0,1)),"CHA":(9,(1,3)),"PER":(12,(2,3))},
        "wolfy"     :{"CON":(14,(1,3)), "STR":(10,(2,3)),"INT":(10,(1,2)),"WIS":(10,(1,2)),"DEX":(10,(2,2)),"LUC":(12,(1,2)),"STA":(13,(2,3)),"SPD":(11,(1,3)),"CHA":(11,(1,2)),"PER":(11,(2,3))}
        }

    listattr=["CON","STR", "DEX", "INT","CHA", "WIS", "PER", "STA", "SPD", "LUC"]

    listrac=list(defattr.keys())

    minipic={
        "human"     :[" (~~~) "," |o o| ","(| . |) "," ( - ) "],
        "undead"    :[" (())) ","/|x x| ","/| . | ","\\( - ) "],
        "elf"       :[" /~~~/ "," |o o| ","\\| . |/"," \\ - / "],
        "ent"       :[" \\#|#/ ","~ \\|/  ","  )|( ~","  )|(  "],
        "goblin"    :["/(-'-)\\","\\/   \\/","/o. .o\\","\\  i  /"],
        "wolfy"     :[" /\\-/\\ ","((o o))","\\ /_\\ /"," \\_-_/ "],
        "orc"       :["<\\<,>/>","( 0 0 )","\\ ),( /"," \\=-=/ "],

    }



    listcard=["North","South","East","West"]

    deftal={
        "Jack of all trades":("When leveling up, each base stat is increased by one more",1),
        "MC Dodger":("Can't touch this!",1),
        "Resilient": ("It's just a scratch",1),
        "Divine Spark": ("Even death won't kill me!",1),
        "Smart Goblin": ("Money! Money! Money!",1),
        "Intangible": ("Not really there",1),
        "Giant": ("I would explain, but you are very small",1),
        "Bulky": ("I've seen many battles",1),
        "Clever": ("I've seen things beyond your comprehension",1),
        "Scholar": ("Books are my friends",1),
        "Etherborn": ("Magic is my ally",1),
        "Lucky": ("Heads i win, tails they lose",1),
        "Prepared": ("I always carry my potions with me",1),
        "Beginner's luck": ("I never found any Four Leaves Clover, they always have more", 1),
        "Backstabber": ("No matter how you face me, i'm going to stab you in the back",1),
        "Leprechaun": ("I'm lucky and i know it",1)
        }

    listtal=list(deftal.keys())

    '''
    CON : Max HP
    STR : Phys Damage
    INT : Max MP
    WIS : Magic Dodge
    Dex : Phys Dodge
    Luc : Used in encounters
    STA : Generic Damage Reduce
    SPD : Attack speed
    ??? : Magic Damage
    '''

    prettyname={
        "lpot":"\33[38;2;210;236;134mLife\33[0m potion",
        "mpot":"\33[38;2;137;177;210mMana\33[0m potion",
        "spdb":"🥾 Speed Boots",
        "dglo":"🧤 Dexterity Gloves",
        "what":"🎩 Wizard Hat",
        "lche":"🦺 Life Chest",
        "samu":"📿 Sage Amulet",
        "4lc":"🍀 Four leaf Clover",
        "sshi":"🔰 Small shield"
        }

    liststuff=list(prettyname.keys())
    liststuff.remove("lpot")
    liststuff.remove("mpot")

    def __init__(self,name,race,sex="x"):
        self.name   = name
        self.race   = race
        self.prace  = Perso.prace(race)
        self.attr={}
        for i in Perso.listattr:
            self.attr[i] = [Perso.defattr[race][i][0],0]
        self.xp     = 0
        self.lvl    = 1
        self.sex    = sex
        self.gold   = 0
        self.nbdod  = 0
        self.nbkill = 0
        self.nbinit = 0
        self.alive  = 1
        self.items  = []
        self.tallist= []
        self.bpd    = 0
        self.bmd    = 0
        self.brdc   = 0
        self.bhp    = 0
        self.bghp   = 0
        self.bmp    = 0
        self.bgmp   = 0
        self.bfa    = 0
        self.bchance= 0

        self.nbach  = 0
        self.lidod  = [5,10,25,50,100,250,500,1000]
        self.lifsa  = [5,10,25,50,100,250,500,1000]
        self.lifig  = [5,10,25,50,100,250,500,1000]


        if race=="undead":
            self.alive += 1
        tal = random.choice(Perso.listtal)
        self.newtal(tal)
        self.welcom(tal)

    def prace(race):
        if race in PrettyUI.racecol:
            return PrettyUI.add_color(race, PrettyUI.racecol[race])
        return race

    def achiev(self,list,s="an"):
        list.pop(0)
        self.nbach += 1
        print("You completed {} achievement, here's a little boost for you".format(s))

    def welcom(self,tal):
        print ("Welcome {}. You are a young {} ready for an adventure. You have been blessed with {}. \n [{}]: {}. \n Here we go...".format(
                self.name, self.prace, tal, self.name, Perso.deftal[tal][0]))

    def printtal(tallist):
        print("\n\tYou had the following talent{}:".format(PrettyUI.ans(len(tallist))))
        s="\t -  "
        s+=',\n\t -  '.join(tallist)+"."
        print(s)

    def printite(items):
        n=len(items)
        lit =[Perso.prettyname[x] for x in items]
        if n>0:
            print("\n\tYou had the following item{}:".format(PrettyUI.ans(n)))
            s="\t -  "
            s+=',\n\t -  '.join(lit)+"."
            print(s)

    def printattr(self):
        b=0
        s=""
        for i in Perso.listattr:
            b+=1
            if b%3==1:
                s+=" "+PrettyUI.add_color(Perso.minipic[self.race][b//3],PrettyUI.racecol[self.race])+"\t"
            s+=" "+i+" "+str(self.attr[i][0])+"\t \t"
            if b%3==0:
                s+="\n"
        print(s)


    def newtal(self,tal,fill=True):
        Perso.listtal.remove(tal)
        if tal == "Divine Spark":
            self.alive +=1
        elif tal == "Smart Goblin":
            self.gold +=100
        elif tal == "Lucky":
            self.attr["LUC"][1]+=3
        elif tal == "Beginner's luck":
            self.attr["LUC"][0]+=10
        elif tal == "Backstabber":
            self.bfa += 2
        elif tal == "Leprechaun":
            self.bchance += 5
        elif tal == "Prepared":
            self.items.append("lpot")
            self.items.append("mpot")
        elif tal == "MC Dodger":
            self.bpd += 5
        elif tal == "Resilient":
            self.brdc += 2
        elif tal == "Intangible":
            self.bpd += 2
            self.bmd += 2
        elif tal == "Giant":
            self.bghp += 5
        elif tal == "Bulky" :
            self.bhp += 100
        elif tal == "Scholar":
            self.bgmp += 5
        elif tal == "Clever":
            self.bmp += 100
        elif tal == "Etherborn":
            self.bmd += 5
        elif tal == "Jack of all trades":
            for k in list(self.attr.keys()):
                self.attr[k][1]+=1
        self.tallist.append(tal)
        self.update(fill)

    def newitem(self,item,fill=True):
        Perso.liststuff.remove(item)
        if item == "spdb":
            self.attr["SPD"][0]+=3
        elif item == "dglo":
            self.attr["DEX"][0]+=3
        elif item == "what":
            self.attr["INT"][0]+=3
        elif item == "lche":
            self.attr["CON"][0]+=3
        elif item == "samu":
            self.attr["WIS"][0]+=3
        elif item == "4lc":
            self.attr["LUC"][0]+=3
        elif item == "sshi":
           self.attr["STA"][0]+=3
        self.items.append(item)
        self.update(False)

    def update(self,fill=True):  # Updates the dodge, red and so on for each level
       self.pdodge  = min(int((self.attr["DEX"][0])/self.lvl**0.5)+self.bpd,75)
       self.mdodge  = min(int((self.attr["WIS"][0])/self.lvl**0.5)+self.bmd,75)
       self.reduce  = min(int((max(0,self.attr["STA"][0] - self.lvl)/self.lvl)**0.4)+self.brdc,75)
       self.maxhp   = (15+self.bghp) * self.attr["CON"][0] +self.bhp
       self.maxmp   = (15+self.bgmp) * self.attr["INT"][0] +self.bmp
       self.chance  = min(75, int(10*(max(0,self.attr["LUC"][0]-self.lvl)**0.4))/10)
       self.fa      = min(int(self.attr["SPD"][0]/self.lvl**0.2+self.bfa),75)
       if fill:
           self.hp      = self.maxhp
           self.mp      = self.maxmp

    def __str__(self):
        return "{} ({}): \33[38;2;210;236;134mLife\33[0m: {} \t \33[38;2;137;177;210mMana\33[0m: {} \t XP: {}/{} \t \t \33[38;2;212;175;55mGold\33[0m: {}".format(
                self.name, self.lvl, Perso.colhp(self.hp,self.maxhp), Perso.colhp(self.mp,self.maxmp), self.xp,
                Perso.xp2lvl(self.lvl), self.gold)

    def colhp(hp,mhp):
        if 10*hp > 9 *mhp:
            return PrettyUI.add_color(hp, PrettyUI.OKGreen)
        elif 10*hp < mhp:
            return PrettyUI.add_color(hp, PrettyUI.Danger)
        elif 3*hp < mhp:
            return PrettyUI.add_color(hp, PrettyUI.Critical)
        return str(hp)

    def nblife(self):
        s = "\33[38;2;212;175;55m"+"☥" * (self.alive-1)+"\33[0m\t"
        s += "\33[38;2;210;236;134m❤\33[0m" *self.items.count("lpot")
        s += "\33[38;2;137;177;210m✿\33[0m" * self.items.count("mpot")
        return s

    def printlvl(self):
        print ("[{} ({})] {} \t \t \t \t {} ⚔  \t {} 🤸 \t 💨 {} \t 🏆 {}\n \33[38;2;210;236;134mMaxHP\33[0m: {} \t  \t \33[38;2;137;177;210mMaxMP\33[0m: {} \t \t \33[38;2;212;175;55mGold\33[0m: {} \n".format(
                self.name, self.prace, self.nblife(), self.nbkill, self.nbdod, self.nbinit, self.nbach, self.maxhp, self.maxmp, self.gold))

        self.printattr()

        print("\tP.Dodge: {}% \t \t M.Dodge: {}% \t\tC.dodge: {}% \n\tD.Reduce: {}% \t \t 1st.Att: {}% \t \t Chance: {}%".format(self.pdodge,self.mdodge,self.pdodge*self.mdodge//10/10,self.reduce,self.fa, self.chance))

    def xp2lvl(lvl):
        '''
        Parameters
        ----------
        lvl : int

        Returns
        -------
        The amount of xp needed between lvl and lvl +1
        Why this formula? Because!

        '''
        return 3 * (lvl**2 - 5 * lvl +8)

    def lvlup(self):
        self.xp  -= Perso.xp2lvl(self.lvl)
        self.lvl += 1
        for i in Perso.listattr:
            self.attr[i][0]+=self.attr[i][1]+random.randint(Perso.defattr[self.race][i][1][0],Perso.defattr[self.race][i][1][1])
        Perso.update(self)
        self.hp=self.maxhp
        print("*"*30 +" Congratulations *"+"*"*29)
        Perso.printlvl(self)
        print("*"*31+PrettyUI.seqspider()+"*"*31)
        self.fluff()
        time.sleep(1)

    def newxp(self,xp):
        self.xp+=xp
        if self.xp >= Perso.xp2lvl(self.lvl):
            Perso.lvlup(self)

    def damage(self,dam,name):
        self.hp -= int(dam * (1-self.reduce/100))
        if self.hp<=0:
            print ("Oh no, your character took lethal damage from the "+name+" :(")
            self.alive -=1
            if self.alive>0:
                self.hp = self.maxhp//2

    def dodge(self,t):
        hit = random.randint(0,100)
        res = [self.pdodge>hit,self.mdodge>hit,self.pdodge>hit or self.mdodge>hit][t]
        return res

    def roll(self,att,val=100):
        return random.randint(0,val) < att


    def handlefight(self):
        name, xp, dam, loot, dod = self.fight()
        self.newxp(xp)
        self.nbkill+=1
        self.gold+= loot
        if not(dod):                                            # If not dodged
            if not(self.roll(self.fa,100+self.lvl)):            # If no sneak attack
                self.damage(dam,name)
                if self.alive > 0:
                    print("You fought "+random.choice(listmean)+" "+name+" and won "+str(xp)+" xp, took "+PrettyUI.givemeans(dam,"damage")+" and earned "+PrettyUI.givemeans(loot, "gold")+"!")
                else:
                    self.gold   -=1
                    self.nbkill -=1
                    return
            else:
                 print("You sneaked on "+random.choice(listmean)+" "+name+" and won "+str(xp)+" xp, you also earned "+PrettyUI.givemeans(loot, "gold")+"!")
                 self.nbinit += 1
        else:
            print("You fought a "+name+" and won "+str(xp)+" xp, avoided damage and earned "+str(loot)+" golds!")
            self.nbdod += 1
        print(self)

    def checkachiev(self):
        if self.nbinit == self.lifsa[0]:
            self.bfa += 0.75
            self.achiev(self.lifsa,"a celerity")
        if self.nbkill == self.lifig[0]:
            self.attr[random.choice(Perso.listattr)][0] += 1
            self.achiev(self.lifig,"a slaying")
        if self.nbdod == self.lidod[0]:
            self.bpd += 0.5
            self.bmd += 0.5
            self.achiev(self.lidod,"a dodging")




    def handlencounter(self):
        enclist=[self.alchemist,self.herbalist,self.healer,self.mspring,self.oracle,self.graal,self.osiris,self.blacksmith]
        a=random.choice(enclist)
        a()

    def autopot(self):
        if "lpot" in self.items and self.hp < 0.2 * self.maxhp:
                print("Auto-using a \33[38;2;210;236;134mLife\33[0m potion")
                self.hp += int(0.4*self.maxhp)
                self.items.remove("lpot")

        if "mpot" in self.items and self.mp < 0.2 * self.maxmp:
                print("Auto-using a \33[38;2;137;177;210mMana\33[0m potion")
                self.mp += int(0.4*self.maxmp)
                self.items.remove("mpot")



    def fight(self):
        strinou = Mon.pickmonster(self.lvl)
        xp      = random.randint(max(0,strinou.xp-2),strinou.xp+self.lvl)
        dam     = random.randint(max(0,strinou.dam-5),strinou.dam+self.lvl)
        hit     = self.dodge(strinou.typ)
        loot    = random.randint(max(0,strinou.loot-5),strinou.loot+self.lvl)
        return (strinou.name,xp,dam,loot,hit)

    def get_race():
        request = 'Choose one of the following race: '
        l = [Perso.prace(x) for x in Perso.listrac]
        request += ', '.join(l) + ': '
        while True:
            ra = input(request)
            if ra not in Perso.defattr:
                print('Unknown race!')
            else:
                return ra

    def reduc(self,price):
        race=random.choice(Perso.listrac)
        if self.race == race or self.race=="goblin":
            return int(0.9 * price),race
        return price,race

    def fluff(self):
        s=""
        box="*"*78
        if self.lvl == 6:
            s+=("An invading {} army is coming from the {}, brace yourself".format(Perso.prace(random.choice(Perso.listrac)),random.choice(Perso.listcard)))
            s+="\n"+box
        elif self.lvl == 12:
            s+=("The army is gone, some spooky monsters are coming your way")
            s+="\n"+box
        elif self.lvl == 18:
            s+=("Whaaaat? They are now coming from space?")
            s+="\n"+box
        elif self.lvl == 22:
            s+=("Nagas, why does it have to be Nagas?")
            s+="\n"+box
        elif self.lvl == 24:
            s+=("Void enemies? I should have stayed in bed...")
            s+="\n"+box
        print(s)

    def herbalist(self):
          price = 200
          price,race = self.reduc(price)
          print("You encounter {} {} herbalist".format(random.choice(listshop),Perso.prace(race)))
          if "lpot" in self.items:
              print("Sadly, you already carry a \33[38;2;210;236;134mLife\33[0m potion \33[38;2;210;236;134m❤\33[0m, they cannot sell you a new one")
          elif self.gold < price:
              print("Sadly, you don't have enough \33[38;2;212;175;55mGold\33[0m, they cannot sell you a \33[38;2;210;236;134mLife\33[0m Potion")
          else:
              b=0
              while b<1:
                  a=input("Do you want to buy a \33[38;2;210;236;134mLife\33[0m potion \33[38;2;210;236;134m❤\33[0m for "+str(price)+" \33[38;2;212;175;55mGold\33[0m (y/n)? ")
                  if a in listyes:
                      self.gold-=price
                      self.items.append("lpot")
                      print("Thank you! Be safe!")
                      b=1
                  elif a in listno:
                      print("Oh, a bold one... I'd say you'd come back crawling but we both know you won't")
                      b=1
                  else:
                      print("That's not a valid answer, please remove the arrow from your ear")

    def alchemist(self):
           price = 150
           price,race = self.reduc(price)
           print("You encounter {} {} alchemist".format(random.choice(listshop),Perso.prace(race)))
           if "mpot" in self.items:
               print("Sadly, you already carry a \33[38;2;137;177;210mMana\33[0m potion \33[38;2;137;177;210m✿\33[0m, they cannot sell you a new one")
           elif self.gold < price:
               print("Sadly, you don't have enough \33[38;2;212;175;55mGold\33[0m, they cannot sell you a \33[38;2;137;177;210mMana\33[0m Potion")
           else:
               b=0
               while b<1:
                   a=input("Do you want to buy a \33[38;2;137;177;210mMana\33[0m potion \33[38;2;137;177;210m✿\33[0m for "+str(price)+" \33[38;2;212;175;55mGold\33[0m (y/n)? ")
                   if a in listyes:
                       self.gold-=price
                       self.items.append("mpot")
                       print("Thank you! Be safe!")
                       b=1
                   elif a in listno:
                       print("Oh, a bold one... I'd say you'd come back crawling but we both know you won't")
                       b=1
                   else:
                       print("That's not a valid answer, please remove the arrow from your ear")

    def healer(self):
           price = 150
           price,race = self.reduc(price)
           print("You encounter {} {} healer".format(random.choice(listshop),Perso.prace(race)))
           if self.hp >= self.maxhp:
               print("You are already at full \33[38;2;210;236;134mLife\33[0m, you don't need their help")
           elif self.gold < price:
               print("Sadly, you don't have enough \33[38;2;212;175;55mGold\33[0m, for their service")
           else:
               b=0
               while b<1:
                   a=input("Do you want to be healed back to full \33[38;2;210;236;134mLife\33[0m for "+str(price)+" \33[38;2;212;175;55mGold\33[0m (y/n)? ")
                   if a in listyes:
                       self.gold-=price
                       self.hp=self.maxhp
                       print("Thank you! Be safe!")
                       b=1
                   elif a in listno:
                       print("Oh, a bold one... I'd say you'd come back crawling but we both know you won't")
                       b=1
                   else:
                       print("That's not a valid answer, please remove the arrow from your ear")

    def mspring(self):
            print("You encounter a magic spring")
            if self.mp >= self.maxmp:
                print("Sadly, you are already at Max \33[38;2;137;177;210mMana\33[0m, the spring is useless")
            else:
                b=0
                while b<1:
                    a=input("Do you want to recoved \33[38;2;137;177;210mMana\33[0m from the spring (y/n)? ")
                    if a in listyes:
                        self.mp=self.maxmp
                        print("Aaaah, what a delight!")
                        b=1
                    elif a in listno:
                        print("Ok, you know, there was no trap...")
                        b=1
                    else:
                        print("That's not a valid answer, please remove the arrow from your ear")

    def osiris(self):
                print("You encounter a mystical god")
                if self.gold < 2500:
                    print("Sadly, you don't have enough \33[38;2;212;175;55mGold\33[0m, for their service")
                else:
                    b=0
                    while b<1:
                        a=input("Do you want to buy an \33[38;2;212;175;55mAnkh ☥\33[0m from them for 2500 \33[38;2;212;175;55mGold\33[0m (y/n)? ")
                        if a in listyes:
                            self.alive+=1
                            self.gold -= 2500
                            print("Here it is. Don't worry, i'll see you later anyway!")
                            b=1
                        elif a in listno:
                            print("I can't wait to see you again")
                            b=1
                        else:
                            print("That's not a valid answer, please remove the arrow from your ear")

    def oracle(self):
          price = 2200
          price,race = self.reduc(price)
          print("You encounter {} {} oracle".format(random.choice(listshop),Perso.prace(race)))
          if  len(Perso.listtal) ==0:
              print("You have nothing new to learn")
          elif self.gold < price:
                    print("Sadly, you don't have enough \33[38;2;212;175;55mGold\33[0m, for their service")
          else:
                    b=0
                    while b<1:
                        a=input("Do you want to buy a new random \33[38;2;239;151;208mTalent\33[0m from them for "+str(price)+" \33[38;2;212;175;55mGold\33[0m (y/n)? ")
                        if a in listyes:
                            tal=random.choice(Perso.listtal)
                            self.newtal(tal,False)
                            self.gold -= price
                            print("You learnt {}, congratulations".format(tal))
                            b=1
                        elif a in listno:
                            print("Some people are less talented than others")
                            b=1
                        else:
                            print("That's not a valid answer, please remove the arrow from your ear")

    def blacksmith(self):
          price = 1600
          price,race = self.reduc(price)
          print("You encounter {} {} blascksmith".format(random.choice(listshop),Perso.prace(race)))
          if  len(Perso.liststuff) ==0:
              print("You have nothing new to buy")
          elif self.gold < price:
                    print("Sadly, you don't have enough \33[38;2;212;175;55mGold\33[0m, for their service")
          else:
                    b=0
                    while b<1:
                        a=input("Do you want to buy a new random \33[38;2;239;151;208mItem\33[0m from them for "+str(price)+" \33[38;2;212;175;55mGold\33[0m (y/n)? ")
                        if a in listyes:
                            ite=random.choice(Perso.liststuff)
                            self.newitem(ite,False)
                            self.gold -= price
                            print("You bought {}, congratulations".format(Perso.prettyname[ite]))
                            b=1
                        elif a in listno:
                            print("Some people think it's better to travel light")
                            b=1
                        else:
                            print("That's not a valid answer, please remove the arrow from your ear")

    def graal(self):
          print("You found the \33[38;2;212;175;55mGraal\33[0m!!")
          b=0
          while b<1:
              a=input("Do you want to try your luck to grab it (y/n)? ")
              if a in listyes:
                  res = random.randint(0,100) < self.chance
                  if res:
                      print("You caught it! Behold an \33[38;2;212;175;55mextra\33[0m life!")
                      self.alive += 1
                      self.hp = self.maxhp
                  else:
                      print("Oh no, you failed and took some damage")
                      self.hp -= (random.randint(15,40) * self.maxhp)//100
                      if self.hp <1:
                          self.hp = 1
                          print("Luckily, the \33[38;2;212;175;55mGraal\33[0m prevented this damage from being lethal")
                  b=1
              elif a in listno:
                  print("Some things are better left alone...")
                  b=1
              else:
                  print("That's not a valid answer, please remove the arrow from your ear")

class Mon:

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

        l = len(Mon.limon)
        minslice=min(max(0,lvl-2),l-1)
        maxslice=(min(l, lvl+2))
        return Mon.limon[minslice:maxslice]

    def pickmonster(lvl):
        '''
        Parameters
        ----------
        lvl : int

        Returns
        -------
        monstrinou : a valid monster for the lvl range

        '''
        name = random.choice(Mon.relslice(lvl))
        c = Mon.defmon[name]
        monstrinou = Mon(name,c)
        return monstrinou

def title():
   str = ("  ____              "
   "    _       _      _"
   "_   __       ____   "
   "   ____      ____   "
   "\r\n"
   " / __\"| u      ___ "
   "    |\"|     |\"|   "
   "  \\ \\ / /    U |  "
   "_\"\\ u U|  _\"\\ uU"
   " /\"___|u \r\n"
   "<\\___ \\/      |_\""
   "_|  U | | u U | | u "
   "   \\ V /      \\| |"
   "_) |/ \\| |_) |/\\| "
   "|  _ / \r\n"
   " u___) |       | |  "
   "  \\| |/__ \\| |/__ "
   " U_|\"|_u      |  _ "
   "<    |  __/   | |_| "
   "|  \r\n"
   " |____/>>    U/| |\\"
   "u   |_____| |_____| "
   "  |_|        |_| \\_"
   "\\   |_|       \\___"
   "_|  \r\n"
   "  )(  (__).-,_|___|_"
   ",-.//  \\\\  //  \\"
   "\\.-,//|(_       // "
   "  \\\\_  ||>>_     _"
   ")(|_   \r\n"
   " (__)      \\_)-\' "
   "\'-(_/(_\")(\"_)(_\""
   ")(\"_)\\_) (__)     "
   "(__)  (__)(__)__)   "
   "(__)__) ")
   print(str)

listmean = ["a mean","a wild","an horrible","a scary","a nasty","a cryptic","a bloody","an evil","a strong","a brooding"]
listshop = ["a traveling","a lost","a friendly","an exhausted","a curious","a clumsy","an interested","an enigmatic"]


def save_per_to_file(self):
    with open('Silly_save.sav', 'wb') as save_file:
        pickle.dump(self, save_file)

def load_per_from_file():
    with open('Silly_save.sav', 'rb') as load_file:
        per = pickle.load(load_file)
        return per

def play(t=0.2):
    title()
    b = False
    if os.path.isfile('./Silly_save.sav'):
        g = True
        while g:
            a = input("Save file detected do you want to load it (y/n)? (Refusing will overwrite it) ")
            if a in listyes:
                b = True
                g = False
            elif a in listno:
                g = False

    if b :
        print("Loading...")
        global per
        per = load_per_from_file()

    else :
        n=input("Please, enter your character name: ")
        r=Perso.get_race()
        per=Perso(n,r)

    per.printlvl()
    time.sleep(10*t)

    while (per.alive > 0):
        per.handlefight()
        if per.alive > 0 and per.roll(per.nbkill % 17,20):
            per.handlencounter()
        per.checkachiev()
        per.autopot()
        time.sleep(t)
        if per.nbkill % 23 == 0:
            save_per_to_file(per)

    if per.alive <1:
        print("/"+"=-"*37+"=\\")
        print("Your lvl {} {} {} died :(".format(per.lvl, per.prace, per.name))
        per.printlvl()
        Perso.printtal(per.tallist)
        Perso.printite(per.items)
        print("\\"+"=-"*15+PrettyUI.seqspider()+"-"+"=-"*14+"=/")
        if os.path.isfile('./Silly_save.sav'):
            os.remove("./Silly_save.sav")
    else:
        print("You stopped your adventure, good bye.")

t=0.1

if len(sys.argv) > 1:
    t=int(sys.argv[1])/10
play(t)
