# -*- coding: utf-8 -*-
"""
Initially done by Olivier Blazy
This does not aim to be anything wonderful
"""

import random
import time

class PrettyUI:
    
    
    racecol={"human":(120,120,240),
             "elf":(80,230,80),
             "orc":(200,120,120),
             "undead":(200,10,200),
             "ent":(170,120,120)}
    
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
    
class Perso:
    defattr={
        "human":{"CON":(10,(1,2)), "STR":(10,(1,2)),"INT":(10,(1,2)),"WIS":(10,(1,2)),"DEX":(10,(1,2)),"LUC":(10,(1,2)),"STA":(10,(1,2))},
        "undead":{"CON":(8,(0,2)), "STR":(11,(2,3)),"INT":(9,(1,1)),"WIS":(12,(0,1)),"DEX":(8,(1,1)),"LUC":(10,(1,2)),"STA":(14,(1,3))},
        "elf":{"CON":(9,(0,1)), "STR":(8,(1,1)),"INT":(8,(2,3)),"WIS":(13,(3,4)),"DEX":(25,(3,6)),"LUC":(10,(3,4)),"STA":(11,(1,2))},
        "orc":{"CON":(15,(2,3)), "STR":(10,(3,4)),"INT":(10,(0,1)),"WIS":(10,(0,1)),"DEX":(10,(0,1)),"LUC":(10,(0,1)),"STA":(15,(2,3))},
        "ent":{"CON":(15,(3,3)), "STR":(10,(2,2)),"INT":(10,(1,2)),"WIS":(10,(0,1)),"DEX":(10,(0,1)),"LUC":(8,(0,1)),"STA":(12,(1,3))}
        }
    
    listattr=["CON","STR","INT","WIS","DEX","LUC","STA"]
    
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
        "Prepared": ("I always carry my potions with me",1)
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
    ??? : Magic Damage
    '''
    
    prettyname={
        "lpot":"\33[38;2;210;236;134mLife\33[0m potion",
        "mpot":"\33[38;2;137;177;210mMana\33[0m potion"
        }
    
    def __init__(self,name,race="human",sex="x"):
        self.name=name
        self.race=race
        self.prace=Perso.prace(race)
        self.attr={}
        for i in Perso.listattr:
            self.attr[i]=Perso.defattr[race][i][0]
        self.xp=0
        self.lvl=1
        self.sex=sex
        self.alive=1
        self.gold=0
        self.nbdod=0
        self.nbkill=0
        self.items = []
        tal=random.choice(Perso.listtal)
        self.tallist=[]
        if race=="undead":
            self.alive +=1
        Perso.newtal(self,tal)
        Perso.update(self)
        Perso.welcom(self,tal)
    
    def prace(race):
        if race in PrettyUI.racecol:
            return PrettyUI.add_color(race, PrettyUI.racecol[race])
        return race
    
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
        
    def newtal(self,tal):
        if tal=="Divine Spark":
            self.alive +=1
        if tal=="Smart Goblin":
            self.gold +=100
        if tal=="Lucky":
            self.attr["LUC"]+=10
        if tal=="Prepared":
            self.items.append("lpot")
            self.items.append("mpot")
        self.tallist.append(tal)
   
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
        s = "\33[38;2;212;175;55m"+"☥"*(self.alive-1)+"\33[0m"
        return s
   
    def printlvl(self):
        print ("[{} ({})] {} \n \33[38;2;210;236;134mMaxHP\33[0m: {} \t  \t \33[38;2;137;177;210mMaxMP\33[0m: {} \t \t \33[38;2;212;175;55mGold\33[0m: {} \n STR {} \t \t \t INT {}  \t \t \t WIS {} \n DEX {}  \t \t \t LUC {} \t \t \t STA {}".format(
                self.name, self.prace, self.nblife(), self.maxhp, self.maxmp, self.gold, self.attr["STR"], self.attr["INT"], self.attr["WIS"], self.attr["DEX"], self.attr["LUC"], self.attr["STA"]))

        print("\tP.Dodge: {}% \t \t M.Dodge: {}% \n\tC.dodge: {}% \t \t D.Reduce: {}%".format(self.pdodge,self.mdodge,self.pdodge*self.mdodge//10/10,self.reduce))  
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
        self.xp -= Perso.xp2lvl(self.lvl)
        self.lvl += 1
        b=0
        if "Jack of all trades" in self.tallist:
            b=1
        for i in Perso.listattr:
            self.attr[i]+=b+random.randint(Perso.defattr[self.race][i][1][0],Perso.defattr[self.race][i][1][1])
        Perso.update(self)
        self.hp=self.maxhp
        print("*"*30 +" Congratulations *"+"*"*30)
        Perso.printlvl(self)
        print("*"*78)
        time.sleep(1)
        
    def newxp(self,xp):
        self.xp+=xp
        if self.xp >= Perso.xp2lvl(self.lvl):
            Perso.lvlup(self)
    
    def update(self):  # Updates the dodge, red and so on for each level
        p=0
        m=0
        r=0
        hp=0
        ghp=0
        mp=0
        gmp=0
        if "MC Dodger" in self.tallist:
            p+=5
        if "Resilient" in self.tallist:
            r+=2
        if "Intangible" in self.tallist:
            p+=2
            m+=2
        if "Giant" in self.tallist:
            ghp+=5
        if "Bulky" in self.tallist:
            hp+=100
        if "Scholar" in self.tallist:
            gmp+=5
        if "Clever" in self.tallist:
            mp+=100
        if "Etherborn" in self.tallist:
            m+=5
        self.pdodge = min(int((self.attr["DEX"])/self.lvl**0.5)+p,75)
        self.mdodge = min(int((self.attr["WIS"])/self.lvl**0.5)+m,75)
        self.reduce = min(int((self.attr["STA"] - self.lvl)/self.lvl**0.4)+r,75)
        self.maxhp = (15+ghp) * self.attr["CON"] +hp
        self.hp=self.maxhp
        self.maxmp = (15+gmp) * self.attr["INT"] +mp
        self.mp=self.maxmp
    
    def damage(self,dam,name):
        self.hp -= dam
        if self.hp<=0:
            print ("Oh no, your character took lethal damage from a "+name+" :(")
            self.alive-=1
            if self.alive>0:
                self.hp = self.attr["CON"]*5 + self.lvl
            
    def dodge(self,t):
        hit = random.randint(0,100)
        res = [self.pdodge>hit,self.mdodge>hit,self.pdodge>hit or self.mdodge>hit][t] 
        return res
            
    def fight(self):
        strinou=Mon.pickmonster(self.lvl)
        xp=random.randint(max(0,strinou.xp-2),strinou.xp+self.lvl)
        dam = random.randint(max(0,strinou.dam-5),strinou.dam+self.lvl)
        hit = Perso.dodge(self,strinou.typ)
        loot = random.randint(max(0,strinou.loot-5),strinou.loot+self.lvl)
        return (strinou.name,xp,dam,loot,hit)

    def get_race():
        request = 'Choose one of the following race: '
        l = [Perso.prace(x) for x in Perso.defattr.keys()]
        request += ', '.join(l) + ': '
        while True:
            ra = input(request)
            if ra not in Perso.defattr:
                print('Unknown race!')
            else:
                return ra           
      
                
        
    def herbalist(self):
          print("You encounter a traveling {} herbalist".format(Perso.prace(random.choice(list(Perso.defattr.keys())))))
          if "lpot" in self.items:
              print("Sadly, you already carry a \33[38;2;210;236;134mLife\33[0m potion, they cannot sell you a new one")
          elif self.gold < 200:
              print("Sadly, you don't have enough \33[38;2;212;175;55mGold\33[0m, they cannot sell you a \33[38;2;210;236;134mLife\33[0m Potion")
          else:
              b=0
              while b<1:
                  a=input("Do you want to buy a \33[38;2;210;236;134mLife\33[0m potion for 200 \33[38;2;212;175;55mGold\33[0m (y/n)? ")
                  if a=="y":
                      self.gold-=200
                      self.items.append("lpot")
                      print("Thank you! Be safe!")
                      b=1
                  elif a=="n":
                      print("Oh, a bold one... I'd say you'd come back crawling but we both know you won't")
                      b=1
                  else:
                      print("That's not a valid answer, please remove the arrow from your ear")
                      
    def alchemist(self):
           print("You encounter a traveling {} alchemist".format(Perso.prace(random.choice(list(Perso.defattr.keys())))))
           if "mpot" in self.items:
               print("Sadly, you already carry a \33[38;2;137;177;210mMana\33[0m potion, they cannot sell you a new one")
           elif self.gold < 150:
               print("Sadly, you don't have enough \33[38;2;212;175;55mGold\33[0m, they cannot sell you a \33[38;2;137;177;210mMana\33[0m Potion")
           else:
               b=0
               while b<1:
                   a=input("Do you want to buy a \33[38;2;137;177;210mMana\33[0m potion for 150 \33[38;2;212;175;55mGold\33[0m (y/n)? ")
                   if a=="y":
                       self.gold-=150
                       self.items.append("mpot")
                       print("Thank you! Be safe!")
                       b=1
                   elif a=="n":
                       print("Oh, a bold one... I'd say you'd come back crawling but we both know you won't")
                       b=1
                   else:
                       print("That's not a valid answer, please remove the arrow from your ear")
                       
    def healer(self):
           print("You encounter a traveling {} healer".format(Perso.prace(random.choice(list(Perso.defattr.keys())))))
           if self.hp >= self.maxhp:
               print("You are already at full \33[38;2;210;236;134mLife\33[0m, you don't need their help")
           elif self.gold < 150:
               print("Sadly, you don't have enough \33[38;2;212;175;55mGold\33[0m, for their service")
           else:
               b=0
               while b<1:
                   a=input("Do you want to be healed back to full \33[38;2;210;236;134mLife\33[0m for 150 \33[38;2;212;175;55mGold\33[0m (y/n)? ")
                   if a=="y":
                       self.gold-=150
                       self.hp=self.maxhp
                       print("Thank you! Be safe!")
                       b=1
                   elif a=="n":
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
                    if a=="y":
                        self.mp=self.maxmp
                        print("Aaaah, what a delight!")
                        b=1
                    elif a=="n":
                        print("Ok, you know, there was no trap...")
                        b=1
                    else:
                        print("That's not a valid answer, please remove the arrow from your ear")                    
     
    def oracle(self):
          print("You encounter a traveling {} oracle".format(Perso.prace(random.choice(list(Perso.defattr.keys())))))
          print("They are unimpressed")

   
    def graal(self):
          print("You found the \33[38;2;212;175;55mGraal\33[0m!!")
          b=0
          while b<1:
              a=input("Do you want to try your luck to grab it (y/n)? ")
              if a=="y":
                  res = random.randint(0,100)<(self.attr["LUC"]-self.lvl)
                  if res:
                      print("You caught it! Behold an \33[38;2;212;175;55mextra\33[0m life!")
                      self.alive += 1
                      self.hp = self.maxhp
                  else:
                      print("Oh no, you failed and took some damage")
                      self.hp -= random.randint(3, 8)
                      if self.hp <1:
                          self.hp = 1
                          print("Luckily, the \33[38;2;212;175;55mGraal\33[0m prevented this damage from being lethal")
                  b=1
              elif a=="n":
                  print("Some things are better left alone...")
                  b=1
              else:
                  print("That's not a valid answer, please remove the arrow from your ear")      
           
class Mon:
    
    defmon= {"cryptographer":(3,0,1,3), "moth":(1,1,0,0), 
             "butterfly":(2,2,0,1), "bee":(3,3,0,2),
             "bear":(6,7,0,0), "mage":(10,10,1,4), 
             "soldier":(10,10,0,5), "slime":(11,12,1,3),
             "demon":(13,12,2,3), "vampire":(14,15,0,4),
             "elemental":(15,15,1,4), "moon alien":(18,20,2,4)} # Name, base xp, base dmg, phy|mag|chaos, loot
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
        
    
      
    
def play(t=0.2):
    n=input("Enter your character name: ")
    r=Perso.get_race()
    per=Perso(n,r)
    per.printlvl()
    time.sleep(10*t)
#    b='y'
    while (per.alive >0):
        name, xp, dam, loot, hit = per.fight()
        per.newxp(xp)
        if not(hit):
            dam = int(dam * (1-per.reduce/100))
            Perso.damage(per,dam,name)
            if per.alive >0:
                per.nbkill+=1
                print("You fought a "+name+" and won "+str(xp)+" xp, took "+PrettyUI.givemeans(dam,"damage")+" and earned "+PrettyUI.givemeans(loot, "gold")+"!")
                if per.nbkill % 17 == 0 and random.randint(0,50)<per.attr["LUC"]:
                    enclist=[per.alchemist,per.herbalist,per.healer,per.mspring,per.oracle,per.graal]
                    a=random.choice(enclist)
                    a()
                
                if "lpot" in per.items and per.hp < 0.2 * per.maxhp:
                    print("Auto-using a \33[38;2;210;236;134mLife\33[0m potion")
                    per.hp += int(0.4*per.maxhp)
                    per.items.remove("lpot")
                    time.sleep(3*t)
                    
                if "mpot" in per.items and per.mp < 0.2 * per.maxmp:
                    print("Auto-using a \33[38;2;137;177;210mMana\33[0m potion")
                    per.mp += int(0.4*per.maxmp)
                    per.items.remove("mpot")
                    time.sleep(3*t)
                    
        else:
            print("You fought a "+name+" and won "+str(xp)+" xp, avoided damage and earned "+str(loot)+" golds!")
            per.nbdod += 1
        if per.alive >0:
            per.gold+= loot
            print(per)
            time.sleep(t)
    if per.alive <1:
        print("*"+"=-"*37+"=*")
        print("Your lvl {} {} {} died, after dodging {} times and killing {} monsters".format(per.lvl, per.prace, per.name, per.nbdod, per.nbkill))
        per.printlvl()
        Perso.printtal(per.tallist)
        Perso.printite(per.items)
    else:
        print("You stopped your adventure, good bye.")
        
play(0.01)