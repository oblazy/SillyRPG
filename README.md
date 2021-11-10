# SillyRPG
A Silly Terminal RPG
<pre>
  ____                  _       _      __   __       ____      ____      ____   
 / __"| u      ___     |"|     |"|     \ \ / /    U |  _"\ u U|  _"\ uU /"___|u 
<\___ \/      |_"_|  U | | u U | | u    \ V /      \| |_) |/ \| |_) |/\| |  _ / 
 u___) |       | |    \| |/__ \| |/__  U_|"|_u      |  _ <    |  __/   | |_| |  
 |____/>>    U/| |\u   |_____| |_____|   |_|        |_| \_\   |_|       \____|  
  )(  (__).-,_|___|_,-.//  \\  //  \\.-,//|(_       //   \\_  ||>>_     _)(|_   
 (__)      \_)-' '-(_/(_")("_)(_")("_)\_) (__)     (__)  (__)(__)__)   (__)__) 
 </pre>

## A little story
You're an adventurer in a wonderland, and are chasing monsters to find gold and treasures...

![image](https://user-images.githubusercontent.com/23337944/140618001-2fb310cc-f1f7-4e17-a2b9-18842887899e.png)

## How to play

- Launch the rpg.py file. 
- (it should auto launch the function play())
- An optinal argument exist to determine the speed of the program. 0 is the fastest, 1 is normal, more is slower
- Watch the screen and decide your fate :)

## Troubleshooting:

- Missing module? There are some dependencies, maybe you are missing one? (sty?)
<pre> pip install sty sys random time pickle os</pre>

- Colors are derpy... We are working on this, please tell us which system

- 

## Things to come!

- [X] Interactivity
- [X] New character races
- [X] New monsters
- [X] Talents
- [X] Let the attributes do something (in progress)
- [ ] Cute interface (in progress... ish)
- [ ] Weapons / Stuff ? (ish)
- [ ] Quests
- [ ] Saga
- [X] Auto saving every 23 fights (and can reload)
- [ ] "Protection" on the savefile
- [ ] ???
- [ ] Get the first Nobel Prize for excellence in Video Game dev 
- [ ] or at least a cookie

## Additional Stuff:
- This program uses pickle to read the save file, as such, be careful when downloading save files from an untrusted source. SillyRPG will not intentionnaly harm your computer, but maliciously crafted savefiles can.
- This program has no access to internet, as such we don't read, collect, play with your data. The only extra files generated while playing is your autosave file named "Silly_save.sav". It is automatically deleted when your character dies.
- As we are in early development phases, we don't guarantee compatibility between save files of different version.
- Current run for now last until lv 20-30 so may not take to long :)
