#import libraries
import time
import pygame, math
#initialise the screen
WIDTH = 894
HEIGHT = 630
groundcolour = 255,255,255
groundcolour2 = 120,0,120
#sprite is not drawn and is used as a constant hitbox so that the costume actor can be drawn at the same location as the sprite but it's image can change without the hitbox of the character changing
sprite = Actor('idle1', (300,300))
costume = Actor('idle1', (300,300))
#initialising rain into position (didn't end up using)
raining = []

for b in range(6):
    for l in range(3):
        rain = Actor('rain')
        rain.topleft = l * 315,b * 200 - 800
        raining.append(rain)

#initialising variables

#player movement variables
ycollide = False
gravity = 0
jumping = False
yvel = 8.5
dead2 = False
falling = False
xcollide = False
slidingright = False
slidingleft = False
walljumpleft = False
walljumpright = False
sprint = False
xvel = 0
xvel2 = 0
runright = False
runleft = False
#miscellaneous counter variable used when I need a value to go up
counter = 0

#determines the realm of the player
dimension = True

#forgot what this does
first = False

#crate variables
down = False
mousepos = (0, 0)
moverxvel = 0
moveryvel = 0
release = False
released = False

#unused variables when I was creating a grappling hook
rope = False
sinx = 0
angle = 0

#determine how much the x velocity is currently changing by
xveldiff = 0
yveldiff = 0

#more unused variables for grappling hook
trajectory = False
displacement = 0
ropexvel = 0
ropeyvel = 0
ropeyveldiff = 0
ropexveldiff = 0
center = 0
center2 = 0

#determine if the game is running or not
title = True

#miscellaneous list for use when I need to create a temporary list inside a function
lizt = []

#more crate variables
swing = False
shattered = False
finalpos = 0,0

#unused crouch and sprint variables
crouch = False
sprint = False

#if the door is open or not
opened = False

#animation variables
holding = False
attack = False
cycle = False
cycle2 = False
tester = False

#how fast the player can go left and right
terminalx = 5

#variables for level selector screen
level_selector = False
selected_level = 0

#keeps track of player score and kills for use in generating the Underworld level
kills = 0
score = 0

#crate collisions
totalreleased = False

#toggleable variable so I can select whatever level I want
admin = True

#different screens
setting = False
credit = False

#settings button
settingicon = Actor('settings',(WIDTH,0))
settingicon.topright = WIDTH, 0

#X is for blocks, M is for movers, D is for doors, S is for spikes, E is for enemy, F is for filler blocks
#these were my dev testing levels so I could get everything working
#filler blocks do not have collisions and are for aesthetics, too many normal blocks lags the game
level = [
    "                                                             X        X                                      ",
    "                                                            X         X                                      ",
    "                                                           X          X                                      ",
    "                                                          X           X                 H                    ",
    "                                                         X                              H                    ",
    "                                                        X                               H                    ",
    "                                                       X                                H                    ",
    "                                                  XXXXX            XXXXXXXXXXXXXXXXXX   H                    ",
    "               XXXX                            X   X                  X                 H                    ",
    "         X                          S          X   X                  X                 H     XXXXXXXXXXXX   ",
    "         D                     X  XXXXX        X   X                  X                 H                    ",
    "         D                  X                  X   X                  X                                      ",
    " X       D         BDDDDX                      X   X                  X                                      ",
    " X   E   D  M      X            E              X   X                  X                                      ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   X                                      ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                                   X                                      ",
    "XXXXXXXX                                                              X                                      "
]

level1_alt = [
    "                                                                                               ",
    "                                                                                               ",
    "                                                                                               ",
    "                                                                                               ",
    "    X               XXX                                                                        ",
    "                                                                                               ",
    "                             XXXX                                                              ",
    "    XXXX                                          XXXXXXXXXXXX                                 ",
    "                                          X       X                                            ",
    "                                          X       X                                            ",
    "                               X  XXXXX   X       X                                            ",
    "                            X             X       X                                            ",
    " X                 X    X                 X       X                                            ",
    " X       X         X                      X       X                                            ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                  ",
    "XXXXXXXXXXXXX    XXXXXXXX   XXXXXX                                                             ",
    "XXXXXXXXXXXXX    XXXXXXXX   XXXXXX                                                             "
]

#initialising the lists and variables for all the different types of blocks
blocks = []
blocks2 = []
movers = {}
hooks = []
fillers = []
fillers2 = []
dict = {'1':['test','poo']}
number = 0
number2 = 0
number3 = 0
number4 = 0
number5 = 0
number6 = 0
number8 = 0
number9 = 0
objx = 0
actx = 0
tilesize = 32
dragged = False
hitbox = Rect ((0, 0),(tilesize+2,tilesize+2))
drawn = True
enemies = {}
mxvel = 1
saws = []
number7 = 0
counter2 = 0
numbero3 = 1
portal = Actor('portal',(6500+objx,550))

#initialising animation frames
skele_walk = ['skele1','skele2','skele3','skele4']
skele_death = ['death1','death2','death3','death4']
skele_image = skele_walk
costume_death = ['sdeath1','sdeath2','sdeath3','sdeath4','sdeath5','sdeath6','sdeath7','sdeath8','sdeath9','sdeath10']
costume_hang = ['hang1']
costume_attack = ['attack1','attack2','attack3','attack4']
costume_slide = ['slide1','slide2','slide3']
costume_fall = ['fall1','fall2','fall3']
costume_jump = ['jump1','jump2','jump3']
costume_run = ['run1','run2','run3','run4','run5','run6','run7','run8','run9','run10']
costume_idle = ['idle1','idle2','idle3','idle4','idle5','idle6','idle7','idle8','idle9','idle10']
costume_images = costume_idle
#if the costume is changing this is True
changing = False

placeholder = 'placeholder'

#miscellaneous
left = False
alive = True
dead = False
numbero = 0
numbero2 = 0

#how many levels the player has unlocked
unlocked = 1

#intialising location and lizt of different types of blocks
for t in range(len(level)):
        for i in range(len(level[t])):
            if level[t][i] == 'X':
                blocks.append("block{0}".format(100*t + i))
                blocks[number] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                number += 1
            elif level[t][i] == 'H':
                hooks.append("hook{0}".format(100*t + i))
                hooks[number4] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                number4 += 1
            elif level[t][i] == 'M':
                movers[str(number3)] = ["mover" + str(100 * t + i),moverxvel,moveryvel,released,dragged,shattered,finalpos,hitbox,drawn]
                movers[str(number3)][6] = (i * tilesize, t * tilesize)
                movers[str(number3)][0] = Rect ((i * tilesize, t * tilesize),(tilesize,tilesize))
                number3 += 1
            elif level[t][i] == 'D':
                blocks.append("block{0}".format(100*t + i))
                blocks[number] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                number += 1
            elif level[t][i] == 'B':
                blocks.append("block{0}".format(100*t + i))
                blocks[number] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                number += 1
            elif level[t][i] == 'E':
                enemies[str(number6)] = ["enemy" + str(100 * t + i),mxvel,actx,alive,skele_image]
                enemies[str(number6)][0] = Actor(enemies[str(number6)][4][numbero2], (i * tilesize + enemies[str(number6)][2], t * tilesize))
                number6 += 1
            elif level[t][i] == 'S':
                saws.append("saw{0}".format(100*t + i))
                saws[number7] = Actor('saw', (i * tilesize + objx + 16, t * tilesize + 22))
                number7 += 1
            elif level[t][i] == 'F':
                fillers.append("filler{0}".format(100*t + i))
                fillers[number8] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                number8 += 1

#initialising blocks for alternate dimension
for v in range(len(level1_alt)): #row
        for q in range(len(level1_alt[v])): #column
            #if there's a block in the lizt
            if level1_alt[v][q] == 'X':

                #giving lizt item a name
                blocks2.append("block{0}".format(100*v + q))
                #assign this lizt item as a rectangle in position relative to q and v
                blocks2[number2] = Rect ((q * tilesize + objx, v * tilesize),(tilesize,tilesize))
                #next block item
                number2 += 1
            elif level1_alt[v][q] == 'F':
                fillers2.append("filler{0}".format(100*t + i))
                fillers2[number9] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                number9 += 1

#learning how to set transparency
s = pygame.Surface((950,600))
s.set_alpha(128)
s.fill((0,0,0))
oof = 0


#initialising the buttons
start = Rect ((447,300),(280,50))
start.center = 447,300

settings = Rect ((447,400),(230,50))
settings.center = 447,400



start_colour = "#6A0DAD"
setting_colour = "#6A0DAD"


#this is only temporary, have different music for different situations (ended up as final)
pygame.mixer.pre_init(22050,-16,2,1024)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050,-16,2,1024)
sounds.ost2.play(-1)


#music.play('quartet')

#intialise variables for level selector buttons
spacing = 160
columns = 4
rows = 3
selector1 = Rect ((207,175),(140,100))
selector1.center = 207,175


#create a class of buttons to make my life easier cuz I have a lot to create
class Button:
    def __init__(self, pos, size, name):
        self.name = name
        self.rect = Rect (pos,size)
        self.rect.center = pos
        self.colour = "#6A0DAD"
    def hover(self):
        if self.rect.collidepoint(mousepos):
            self.colour = "#410063"
        else:
            self.colour = "#6A0DAD"
    def drawn(self):
        screen.draw.filled_rect((self.rect),(self.colour))


Return = 'return'
Return = Button((WIDTH/2,335+180),(800,60),Return)

Menu = 'menu'
Menu = Button((60,50),(100,30),Menu)

Sounds = 'Sounds'
Sounds = Button((WIDTH/2,400),(300,50),Sounds)

Back2LS = 'Back2LS'
Back2LS = Button((WIDTH/2,250),(450,50),Back2LS)

ToGame = 'ToGame'
ToGame = Button((WIDTH/2,550),(200,50),ToGame)



"""selector2 = Rect ((selector1.center[0] + spacing,175),(140,100))
selector2.center = selector1.center[0] + spacing,175
selector3 = Rect ((selector2.center[0] + spacing,175),(140,100))
selector3.center = selector2.center[0] + spacing,175
selector4 = Rect ((selector3.center[0] + spacing,175),(140,100))
selector4.center = selector3.center[0] + spacing,175"""

colour = 73, 6, 128
selectors = {}

pee = 0
previous = 0,0
#if sound is on or off
soundcondition = "On"

icon = pygame.image.load('images\purpleblocc.png')
pygame.display.set_caption('The Realms Beyond')
pygame.display.set_icon(icon)

#systematic generation of level selector buttons because individual locations and changing each one is too tedious
for i in range(rows):
    for n in range(columns):
        if n == 0:
            previous = 47
        else:
            previous = selectors[str(n + (i*(columns)))][0].center[0]

        selectors[str(n+1 + (i*(columns)))] = [Rect ((previous+ spacing,175*(i+1)),(140,100)),colour]
        selectors[str(n+1 + (i*(columns)))][0].center = previous + spacing,175*(i+1)



scores = ''

def draw():
    #globalise variables
    global icon, soundcondition, soundname, setting, unlocked, Return, return_colour, credit, number9, number8, scores, score, selected_level, numbero3, level_selector, start_colour, settings_colour, oof, numbero2, attack, slidingright, left, changing, numbero, number7, number, actx, number6, tilesize, number2, dimension, groundcolour, groundcolour2, number3, mousepos, rope, trajectory, level1_alt
    #setup the window title with an icon and title
    pygame.display.set_icon(icon)
    pygame.display.set_caption('The Realms Beyond')
    #reset counting variables
    number = 0
    number2 = 0
    number3 = 0
    number4 = 0
    number6 = 0
    number7 = 0
    number8 = 0
    number9 = 0
    #store score as a string
    scores = "Score: " + str(score)
    screen.fill((120, 0, 120))
    #credits screen
    if credit:
        screen.blit('hbackground',(0,0))
        screen.draw.text("YOU WIN!",
        center=(WIDTH/2,80), width=1000, fontname="vermin", fontsize=80,
        color="#410063", gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
        screen.draw.text("Background and Ground Art: Me",
        center=(WIDTH/2,35+120), width=1000, fontname="vermin", fontsize=35,
        color="#6A0DAD", gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
        screen.draw.text("Other Art: Google",
        center=(WIDTH/2,110+120), width=1000, fontname="vermin", fontsize=35,
        color="#6A0DAD", gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
        screen.draw.text("Sound: Google",
        center=(WIDTH/2,185+120), width=1000, fontname="vermin", fontsize=35,
        color="#6A0DAD", gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
        screen.draw.text("Game Tester #1: Hayden S",
        center=(WIDTH/2,260+120), width=1000, fontname="vermin", fontsize=35,
        color="#6A0DAD", gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
        screen.draw.text("Code: Me",
        center=(WIDTH/2,335+120), width=1000, fontname="vermin", fontsize=35,
        color="#6A0DAD", gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
        #screen.draw.filled_rect(returns, (120, 0, 120))
        #Return.drawn()
        screen.draw.text("Return to Level Selector",
        center=(WIDTH/2,335+180), width=1000, fontname="vermin", fontsize=60,
        color=Return.colour, gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
        #screen.draw.filled_rect(returns, (120, 0, 120))

    else:
        #title screen
        if title and not level_selector:
            screen.blit('hbackground',(0,0))

            screen.draw.text("The Realms Beyond",
            center=(447,175), width=1000, fontname="vermin", fontsize=80,
            color="#410063", gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
            screen.draw.text("Start Game",
            center=(447,300), width=1000, fontname="vermin", fontsize=50,
            color=start_colour, gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
            soundname = "Sounds: " + str(soundcondition)
            screen.draw.text(soundname,
            center=(447,400), width=1000, fontname="vermin", fontsize=50,
            color=settings_colour, gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
        #game
        elif not title:

            #reassign positions of blocks in each dimension
            if not dimension:
                if selected_level != '12':
                    screen.blit('hgrey',(0,0))
                else:
                    screen.blit('hred',(0,0))
                for v in range(len(level1_alt)):
                    for q in range(len(level1_alt[v])):
                        if level1_alt[v][q] == 'X':
                            blocks2[number2] = Rect ((q * tilesize + objx, v * tilesize),(tilesize,tilesize))
                            number2 += 1
                        elif level1_alt[v][q] == 'F':
                            fillers2[number9] = Rect ((q * tilesize + objx, v * tilesize),(tilesize,tilesize))
                            number9 += 1
                #draw transparent blocks
                for q in blocks2:
                    oof = pygame.Surface((tilesize,tilesize))
                    oof.set_alpha(45)
                    oof.fill((120,0,120))
                    screen.blit(oof, q)
                for f in fillers2:
                    oof = pygame.Surface((tilesize,tilesize))
                    oof.set_alpha(45)
                    oof.fill((120,0,120))
                    screen.blit(oof, f)

                for t in range(len(level)):
                    for i in range(len(level[t])):

                        if level[t][i] == 'X':
                            blocks[number] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                            number += 1
                        elif level[t][i] == 'H':
                            hooks[number4] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                            number4 += 1
                        elif level[t][i] == 'M':
                            movers[str(number3)][0] = Rect ((movers[str(number3)][6][0] + objx, movers[str(number3)][6][1]),(tilesize,tilesize))
                            number3 += 1
                        elif level[t][i] == 'D':
                            blocks[number] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                            number += 1
                        elif level[t][i] == 'B':
                            blocks[number] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                            number += 1
                        elif level[t][i] == 'E':

                            enemies[str(number6)][0].topleft = (i * tilesize + enemies[str(number6)][2],t * tilesize-tilesize+13)

                            number6 += 1
                        elif level[t][i] == 'S':
                            saws[number7] = Actor('saw', (i * tilesize + objx + 16, t * tilesize+22))
                            number7 += 1
                        elif level[t][i] == 'F':
                            fillers[number8] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                            number8 += 1
                #underworld gimmick
                if selected_level == '12':
                    for h in range(kills):
                        enemies[str(number6)][0].topleft = ((h+13) * tilesize*2 + enemies[str(number6)][2], 8 * tilesize + 13)
                        number6 += 1

                #draw the blocks for relevant dimension, red for the underworld level
                number = 0
                for t in range(len(level)):
                    for i in range(len(level[t])):
                        if level[t][i] == 'X':
                            screen.draw.filled_rect(blocks[number],groundcolour)
                            if selected_level != '12':
                                screen.blit('greydirt',blocks[number])
                            else:
                                screen.blit('reddirt',blocks[number])
                            number += 1
                        if level[t][i] == 'B':
                            screen.draw.filled_rect(blocks[number],groundcolour)
                            screen.blit('buttonun',(blocks[number][0],blocks[number][1]-6))
                            number += 1
                        elif level[t][i] == 'D' and not opened:
                            screen.draw.filled_rect(blocks[number],groundcolour)
                            screen.blit('door',blocks[number])
                            number += 1
                        elif level[t][i] == 'D' and opened:
                            screen.blit('trans',blocks[number])
                            number += 1

                number = 0
                for t in range(len(level)):
                    for i in range(len(level[t])):
                        if level[t][i] == 'X' and level[t-1][i] != 'X' and level[t-1][i] != 'F':
                            if selected_level != '12':
                                screen.blit('greyblocc',(i * tilesize + objx, t * tilesize))
                            else:
                                screen.blit('redblocc',(i * tilesize + objx, t * tilesize))

                for a in movers:
                    screen.draw.filled_rect(movers[str(a)][0], (0, 0, 255))
                    screen.blit('crate',movers[str(a)][0])

                for f in fillers:
                    if selected_level != '12':
                        screen.blit('greydirt',f)
                    else:
                        screen.blit('reddirt',f)
                for k in hooks:
                    screen.blit('rope',(k.left, k.top))
                if numbero2 + 1 > len(skele_image):
                    numbero2 = 0
                for l in enemies:
                    if enemies[str(l)][3] and enemies[str(l)][1] == 1:

                        screen.blit(pygame.transform.flip((pygame.image.load('images/'+str(enemies[str(l)][4][numbero2])+'.png')),True,False),enemies[str(l)][0].topleft)

                    elif enemies[str(l)][3]:
                        enemies[str(l)][0].draw()
                    else:
                        enemies[str(l)][4] = skele_death
                        enemies[str(l)][0].draw()

                for s in saws:
                    s.draw()





            else:
                #reassigning positions and drawing blocks in selected dimension, drawn translucent if in other dimension
                screen.blit('hbackground',(0,0))
                for t in range(len(level)):
                    for i in range(len(level[t])):
                        if level[t][i] == 'X':
                            blocks[number] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                            number += 1
                        elif level[t][i] == 'H':
                            hooks[number4] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                            number4 += 1
                        elif level[t][i] == 'M':
                            movers[str(number3)][0] = Rect ((movers[str(number3)][6][0] + objx, movers[str(number3)][6][1]),(tilesize,tilesize))
                            number3 += 1
                        elif level[t][i] == 'D':
                            blocks[number] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                            number += 1
                        elif level[t][i] == 'B':
                            blocks[number] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                            number += 1
                        elif level[t][i] == 'E':
                            enemies[str(number6)][0].topleft = (i * tilesize + enemies[str(number6)][2],t * tilesize-tilesize+13)
                            number6 += 1
                        elif level[t][i] == 'F':
                            fillers[number8] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                            number8 += 1


                if selected_level == '12':
                    for h in range(kills):
                        enemies[str(number6)][0].topleft = ((h+20) * tilesize + enemies[str(number6)][2], 8 * tilesize + 13)
                        number6 += 1

                for b in blocks:

                    oof = pygame.Surface((tilesize,tilesize))
                    oof.set_alpha(45)
                    oof.fill((120,120,120))
                    screen.blit(oof, b)
                for f in fillers:

                    oof = pygame.Surface((tilesize,tilesize))
                    oof.set_alpha(45)
                    oof.fill((120,120,120))
                    screen.blit(oof, f)
                for v in range(len(level1_alt)):
                    for q in range(len(level1_alt[v])):
                        if level1_alt[v][q] == 'X':
                            blocks2[number2] = Rect ((q * tilesize + objx, v * tilesize),(tilesize,tilesize))
                            number2 += 1
                        elif level1_alt[v][q] == 'F':
                            fillers2[number9] = Rect ((q * tilesize + objx, v * tilesize),(tilesize,tilesize))
                            number9 += 1


                for q in blocks2:
                    screen.draw.filled_rect(q,groundcolour2)
                    screen.blit('purpledirt',q)
                for v in range(len(level1_alt)):
                    for q in range(len(level1_alt[v])):
                        if level1_alt[v][q] == 'X' and level1_alt[v-1][q] != 'X' and level1_alt[v-1][q] != 'F':
                            screen.blit('purpleblocc',(q * tilesize + objx, v * tilesize))
                for f in fillers2:
                    screen.blit('purpledirt',f)

            #animation
            try:
                placeholder = pygame.image.load('images/'+str(costume_images[numbero])+'.png')
            except:
                numbero = 0

            #flip the costume if in the other direction so I don't have to flip each frame individually in the images folder
            if (left and not slidingleft) or slidingright:
                try:
                    screen.blit(pygame.transform.flip((placeholder),True,False),costume.topleft)
                except:
                    costume.image = costume_images[numbero-1]
                    numbero = 0
            else:
                costume.draw()


            #unused rane
            #for k in raining:
                #k.draw()
            #more animation
            if not changing:
                clock.schedule_unique(nextcostume,0.05)
                changing = True

            #portal and scores drawn
            portal.draw()
            screen.draw.text(scores,
            topleft=(20,20), width=1000, fontname="vermin", fontsize=30,
            color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
            numbero3 = 1
        #level selector screen
        else:
            screen.blit('hbackground',(0,0))
            screen.draw.text("Level Selector",
            center=(447,75), width=1000, fontname="vermin", fontsize=50,
            color="#6A0DAD", gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
            screen.draw.text("Menu",
            center=(60,50), width=1000, fontname="vermin", fontsize=30,
            color=Menu.colour, gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
            numbero3 = 1
            #determine which levels the player can access
            for n in selectors:
                if unlocked >= eval(n):
                    pass
                else:
                    selectors[str(n)][1] = (120, 120, 120)

                #draw all previously generated level selector buttons
                screen.draw.filled_rect(selectors[str(n)][0],selectors[str(n)][1])
                screen.draw.text(str(numbero3),
                center=selectors[str(n)][0].center, width=1000, fontname="vermin", fontsize=50,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
                numbero3 += 1
        if dead2:
            #black screen whilst the player is dead
            screen.fill((0,0,0))
            levelselect = "Level " + str(selected_level)

            if selected_level == '12':
                screen.draw.text(levelselect,
                center=(WIDTH/2,HEIGHT/2), width=1000, fontname="vermin", fontsize=100,
                color="#800000", gcolor="#000000", owidth=1.5, ocolor="white", alpha=40)
                numbero3 = 1
            else:
                screen.draw.text(levelselect,
                center=(WIDTH/2,HEIGHT/2), width=1000, fontname="vermin", fontsize=100,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
                numbero3 = 1
            #name of each level
            if selected_level == '1':
                screen.draw.text("Tutorial",
                center=(WIDTH/2,HEIGHT/2 + 75), width=1000, fontname="vermin", fontsize=50,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
            elif selected_level == '2':
                screen.draw.text("The Basics",
                center=(WIDTH/2,HEIGHT/2 + 75), width=1000, fontname="vermin", fontsize=50,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
            elif selected_level == '3':
                screen.draw.text("Switchin' It Up",
                center=(WIDTH/2,HEIGHT/2 + 75), width=1000, fontname="vermin", fontsize=50,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
            elif selected_level == '4':
                screen.draw.text("Spikes, Skeletons, and Sliding",
                center=(WIDTH/2,HEIGHT/2 + 75), width=1000, fontname="vermin", fontsize=50,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
            elif selected_level == '5':
                screen.draw.text("Try and Keep Up",
                center=(WIDTH/2,HEIGHT/2 + 75), width=1000, fontname="vermin", fontsize=50,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
            elif selected_level == '6':
                screen.draw.text("Moving Back to Go Forwards",
                center=(WIDTH/2,HEIGHT/2 + 75), width=1000, fontname="vermin", fontsize=50,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
            elif selected_level == '7':
                screen.draw.text("Cave",
                center=(WIDTH/2,HEIGHT/2 + 75), width=1000, fontname="vermin", fontsize=50,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
            elif selected_level == '8':
                screen.draw.text("Pick a Path",
                center=(WIDTH/2,HEIGHT/2 + 75), width=1000, fontname="vermin", fontsize=50,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
            elif selected_level == '9':
                screen.draw.text("Slow and Steady",
                center=(WIDTH/2,HEIGHT/2 + 75), width=1000, fontname="vermin", fontsize=50,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
            elif selected_level == '10':
                screen.draw.text("Transport the Crate",
                center=(WIDTH/2,HEIGHT/2 + 75), width=1000, fontname="vermin", fontsize=50,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
            elif selected_level == '11':
                screen.draw.text("Platformer's Nightmare",
                center=(WIDTH/2,HEIGHT/2 + 75), width=1000, fontname="vermin", fontsize=50,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
            elif selected_level == '12':
                screen.draw.text("The Underworld",
                center=(WIDTH/2,HEIGHT/2 + 75), width=1000, fontname="vermin", fontsize=50,
                color="#800000", gcolor="#000000", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1

        #text inside levels, level 12 for the underworld, level 1 for tutorial explanations
        elif selected_level == '12' and not title and not level_selector:
            screen.draw.text("Welcome to the Underworld",
            topleft=(50 + objx,100), width=1000, fontname="vermin", fontsize=30,
            color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
            numbero3 = 1

            screen.draw.text("Every enemy you have killed is here",
            topleft=(50 + objx,130), width=1000, fontname="vermin", fontsize=30,
            color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
            numbero3 = 1
        elif selected_level == '1' and not title and not level_selector:
            screen.draw.text("Use arrow keys to move left and right",
            topleft=(50 + objx,300), width=1000, fontname="vermin", fontsize=30,
            color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
            numbero3 = 1

            screen.draw.text("Welcome to The Realms Beyond. This is the Tutorial Level",
            topleft=(50 + objx,100), width=1000, fontname="vermin", fontsize=30,
            color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
            numbero3 = 1

            screen.draw.text("Use the UP Arrow to jump",
            topleft=(950 + objx,300), width=1000, fontname="vermin", fontsize=30,
            color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
            numbero3 = 1

            screen.draw.text("Hold a direction whilst jumping to move mid-air",
            topleft=(950 + objx,360), width=1000, fontname="vermin", fontsize=30,
            color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
            numbero3 = 1

            screen.draw.text("Run into a wall whilst falling to slide down it",
            topleft=(1800 + objx,300), width=1000, fontname="vermin", fontsize=30,
            color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
            numbero3 = 1

            screen.draw.text("Jump whilst sliding to wall-jump",
            topleft=(2000 + objx,360), width=1000, fontname="vermin", fontsize=30,
            color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
            numbero3 = 1

            #By clicking space, you can transfer your body into a parralel realm to this one, and do the same to get back.

            if dimension:
                screen.draw.text("Click space to hop between realms ",
                topleft=(3000 + objx,120), width=1000, fontname="vermin", fontsize=30,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
                #Each realm is slightly different, so you their differences to your advantage when platforming.
                screen.draw.text("Use differences in realms to help you platform ",
                topleft=(3000 + objx,180), width=1000, fontname="vermin", fontsize=30,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1
                #Ground in an alternate realm will be translucently overlayed into the other.
                screen.draw.text("Translucent surfaces substitute objects in other realms",
                topleft=(3000 + objx,240), width=1000, fontname="vermin", fontsize=30,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1

                screen.draw.text("Be careful however: the grey realm contains danger",
                topleft=(3000 + objx,300), width=1000, fontname="vermin", fontsize=30,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1

                screen.draw.text("Hop to grey realm to progress",
                topleft=(4200 + objx,240), width=1000, fontname="vermin", fontsize=30,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1

            else:
                screen.draw.text("Quick! Use left control to slice the enemy",
                topleft=(3600 + objx,300), width=1000, fontname="vermin", fontsize=30,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1

                screen.draw.text("The grey realm has its perks however",
                topleft=(4200 + objx,180), width=1000, fontname="vermin", fontsize=30,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1

                screen.draw.text("Move the crate onto the button with your cursor to open the door",
                topleft=(4200 + objx,240), width=1000, fontname="vermin", fontsize=30,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1

                screen.draw.text("Be careful of spikes!",
                topleft=(5650 + objx,360), width=1000, fontname="vermin", fontsize=30,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1

                screen.draw.text("Climb into the portal by holding up on the ladders to progress",
                topleft=(6250 + objx,360), width=1000, fontname="vermin", fontsize=30,
                color="#6A0DAD", gcolor="#6A0DAD", owidth=0.25, ocolor="white", alpha=40)
                numbero3 = 1

    #draw a settings icon if they're in a game
    if not title:
        settingicon.draw()


    #settings menu
    if setting:
        screen.blit('hbackground',(0,0))
        screen.draw.text("To Game",
        center=(WIDTH/2,550), width=1000, fontname="vermin", fontsize=50,
        color=ToGame.colour, gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
        screen.draw.text("Settings",
        center=(WIDTH/2,100), width=1000, fontname="vermin", fontsize=80,
        color="#6A0DAD", gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
        screen.draw.text("To Level Selector",
        center=(WIDTH/2,250), width=1000, fontname="vermin", fontsize=50,
        color=Back2LS.colour, gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
        soundname = "Sounds: " + str(soundcondition)
        screen.draw.text(soundname,
        center=(WIDTH/2,400), width=1000, fontname="vermin", fontsize=50,
        color=Sounds.colour, gcolor="#6A0DAD", owidth=1.5, ocolor="white", alpha=40)
def nextcostume():
    global dead, numbero2, cycle, cycle2, left, numbero, changing, xvel, placeholder, attack, costume_images, costume_idle
    #animation
    if attack and not cycle:
        cycle = True
        numbero = 0
    if dead and not cycle2:
        cycle2 = True
        numbero = 0

    if numbero > len(costume_images):
        numbero = 0
        attack = False
    costume.image = costume_images[numbero]
    for e in enemies:
        if numbero2 + 1 > len(enemies[str(e)][4]):
            numbero2 = 0

        if enemies[str(e)][0].image == 'death4':
            pass
        else:
            enemies[str(e)][0].image = enemies[str(e)][4][numbero2]

    numbero += 1
    numbero2 += 1
    if costume.image == 'attack4':
        attack = False
        cycle = False

    if costume.image == 'sdeath10':
        dead = False
        cycle2 = False

    changing = False


def update():
    global credit, title, objx, setting, Menu, admin, unlocked, credit, xvel, gravity, dead2, portal, fillers, score, kills, selected_level, level_selector, start_colour, settings_colour, title, xvel, yvel, cycle, attack, left, counter2, number5, objx, groundcolour, groundcolour2, slidingleft, slidingright, mousepos, down, counter, release, rope, actx, enemies, blocks, dead
    global number
    #screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    #admin for game testing and demonstrating

    if admin:
        unlocked = 100



    if not setting:
        if not credit:
            if not title:

                #game
                #execute all created functions
                move()
                raintime()
                #move the costume to the location of the hitbox/sprite
                costume.x = sprite.x
                costume.y = sprite.y

                #move teh crates
                movermove()

                #next level
                if sprite.colliderect(portal):
                    if selected_level != '12':
                        if str(unlocked) == selected_level:
                            unlocked += 1
                        selected_level = str(eval(selected_level) + 1)
                        sprite.x = 300
                        sprite.y = 300
                        title = True
                        dead2 = True
                        clock.schedule_unique(create_level, 1.0)
                    else:
                        #roll the credits if they win
                        credit = True
                        title = True



                #crates moved to assigned position
                for m in movers:
                    movers[str(m)][0].center = movers[str(m)][6]

                #move the enemies left and right, kill them if the player attacks them, kill the player if they hit the enemy
                for e in enemies:
                    for o in blocks:
                        if enemies[str(e)][0].colliderect(o):

                            enemies[str(e)][1] *= -1

                            break
                    if sprite.colliderect(enemies[str(e)][0]) and not dimension and not attack and enemies[str(e)][3] and not dead:
                        death()
                    elif attack and costume.colliderect(enemies[str(e)][0]) and enemies[str(e)][3] and not dimension:
                        enemies[str(e)][3] = False
                        if soundcondition == "On":
                            music.play_once('skeledeath')
                        if selected_level != '12':
                            kills += 1
                        score += 1000
                    if enemies[str(e)][3]:
                        enemies[str(e)][2] -= enemies[str(e)][1]


                #kill player if touching spikes
                for s in saws:
                    if sprite.colliderect(s) and not dimension and not dead:
                        death()

                #move the crate
                if down:
                    for m in movers:

                        if movers[str(m)][4]:
                            poo = list(movers[str(m)][6])
                            poo[0] = mousepos[0] - objx
                            poo[1] = mousepos[1]
                            movers[str(m)][6] = tuple(poo)

                #stop player from moving whilst dead
                if dead:
                    xvel = 0
                    yvel = 0

                #special portal for entry into underworld
                if selected_level == '11':
                    portal.image = ('redportal')
                else:
                    portal.image = ('portal')

                #autoscroll kill player if offscreen
                if selected_level == '9' or selected_level == '5':
                    if sprite.right < 0 and not dead:
                        death()
                    scroll_right()


            #buttons for title screen
            elif not level_selector:
                if start.collidepoint(mousepos):
                    start_colour = "#000000"
                else:
                    start_colour = "#6A0DAD"

                if settings.collidepoint(mousepos):
                    settings_colour = "#000000"
                else:
                    settings_colour = "#6A0DAD"

            else:
                #buttons for level selector screen
                Menu.hover()
                for n in selectors:
                    if selectors[str(n)][0].collidepoint(mousepos):
                        selectors[str(n)][1] = 255, 255, 255
                    else:
                        selectors[str(n)][1] = 73, 6, 128
        else:
            #credits button
            Return.hover()
    else:
        #settings buttons
        Back2LS.hover()
        ToGame.hover()
        Sounds.hover()

#unused rain
def raintime():
    for rain in raining:
        rain.y += 10
        if rain.top > 600:
            rain.top = -350

#blocks move left if the player goes too far to the right
def scroll_left():
    global objx, xvel, xveldiff, actx, mxvel, terminalx, selected_level
    if selected_level == '9' or selected_level == '5':
        pass
    else:
        if not xcollidecheck(-(xvel+xveldiff)) and not xcollidecheck2(-(xvel+xveldiff)):
            objx -= xvel
            portal.x -= xvel
            for e in enemies:
                enemies[str(e)][2] -= xvel


        if xvel < terminalx:
            xvel += 0.25
            xveldiff = 0.25

#create a new level
def create_level():
    global dimension, hooks, title, dead2, number9, number2, fillers2, number8, fillers, level, level1_alt, selected_level, blocks, enemies, number, number2, number3, number4, number5, number6, number7, numbero, numbero2, numbero3, movers, saws, objx, blocks2,hook
    #THERE MUST BE AT LEAST ONE MOVER AND LADDER PER LEVEL OR ELSE THE CODE DOES NOT WORK (for loops in collidechecks)
    #reset variables
    blocks = []
    enemies = {}
    movers = {}
    fillers = []
    hooks = []
    number = 0
    number2 = 0
    number3 = 0
    number4 = 0
    number6 = 0
    number7 = 0
    number8 = 0
    saws = []
    hooks = []
    blocks2 = []
    objx = 0
    fillers2 = []
    number9 = 0
    sprite.x = 300
    sprite.y = 300
    portal.x = 6500
    portal.y = 500
    dimension = True


    #levels
    if selected_level == '1':
        #LEVEL 1
        portal.x = 6500
        portal.y = 500
        level = [
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                            X                                                        ",
            "                                                                                                                                                            D                                                        ",
            "                                                                                                                                                            D                                                        ",
            "                                                                                                                                                            D                                                        ",
            "                                                                             XX                                   X       E          X          M           D                                                        ",
            "                                                                             XX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXBXXXXXXXXX                                                     ",
            "                                                                             XX    XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXX                                                  ",
            "                                                                             XX    XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXX                                   H           ",
            "                                                                             XXXX  XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXX                                H           ",
            "                                                 XXXXX  XXXXX  XXXXX               XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXX                             H           ",
            "                                            XXXXXXXXXX  XXXXX  XXXXXXXXXX          XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXX      S                               ",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    "
        ]
        #LEVEL 1
        level1_alt = [
            "                                                                                                                                                                 ",
            "                                                                                                                                                                 ",
            "                                                                                                                                                                 ",
            "                                                                                                                                                                 ",
            "                                                                                                                                                                 ",
            "                                                                                                                                                                 ",
            "                                                                                                                                                                 ",
            "                                                                                                                                                                 ",
            "                                                                                                                                                            X    ",
            "                                                                                                                                                            X    ",
            "                                                                                                                                                            X    ",
            "                                                                                                                                                            X    ",
            "                                                                             XX                                                                             X    ",
            "                                                                             XX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX              XXXXXXXXXXXXXXXXXXXXXXXXXX    ",
            "                                                                             XX    XXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX              XFFFFFFFFFFFFFFFFFFFFFFFFX    ",
            "                                                                             XX    XXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX              XFFFFFFFFFFFFFFFFFFFFFFFFX    ",
            "                                                                             XXXX  XXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX              XFFFFFFFFFFFFFFFFFFFFFFFFX    ",
            "                                                 XXXXX  XXXXX  XXXXX               XXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX              XFFFFFFFFFFFFFFFFFFFFFFFFX    ",
            "                                            XXXXXXXXXX  XXXXX  XXXXXXXXXX          XXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX              XFFFFFFFFFFFFFFFFFFFFFFFFX    ",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX              XFFFFFFFFFFFFFFFFFFFFFFFFX    "
        ]
    elif selected_level == '6':
        #LEVEL 6
        portal.x = 6500
        portal.y = 500
        level = [
            "                                                                                                                                              X                                                                      ",
            "                                                                                                                                              X                                                                      ",
            "                                                                                                                                              X                                                                      ",
            "                                                                                                                                              X                                                                      ",
            "                                                                              X                                                               X                                                                      ",
            "                                                                      SSS     X         XX     S     XX                                       X                                                                      ",
            "                                                                      XXXXX   X              XXXXX                                            X                                                                      ",
            "                                                                          X   X                                                               X                            X   XXXX                     S            ",
            "                                                                          X   X                                                               X                            X                            X            ",
            "                                                                          X   X                                            X    E     E   X   X                            X   S                        X            ",
            "                                          XXXX                            X   X                                            XXXXXXXXXXXXXXXX   X                                X                        X    S       ",
            "                                   XXXX                                       X                                                               X                            S   X                XXXXX   X    X       ",
            "                                                                              X               SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS         X                  X         X   X                    X   X    X       ",
            "                                                                                              XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX         X                  D         X                        X   X    X       ",
            "XXXXXXXXXXXXXXXXXXXXX                                                                                                                         X                  D         X                        X        X       ",
            "XFFFFFFFFFFFFFFFFFFFX                                                                                                                         D                  D                                  X        X       ",
            "XFFFFFFFFFFFFFFFFFFFX                                                                                                                         D                  D                                  X        X       ",
            "XFFFFFFFFFFFFFFFFFFFX                                                                                 SS M      SS SS  S  SS  SS              D                  XXXXX                              X   XX   X       ",
            "XFFFFFFFFFFFFFFFFFFFX                                                                                 XXXXXXXXXXXXXXXXXXXXXXXXXXXXX           D         XXXXX                                       X    X   X       ",
            "XFFFFFFFFFFFFFFFFFFFX                                                                                       FFFFFFFFFFFFFFFFFFFFFFFXXXBXXX    XXXXXX                                                X    XXXXX                   H"
        ]
        #LEVEL 6
        level1_alt = [
            "                                                                                                                                              X                                                                      ",
            "                                                                                                                                              X                                                                      ",
            "                                                                                                                                              X                                                                      ",
            "                                                                                                                                              X                                                                      ",
            "                                                                              X    XX                                                         X                                                                      ",
            "                                                                              X                                                               X                                                                      ",
            "                                                                              X                                      X                        X                                                                      ",
            "                                                                              X                            XX   X                             X                                                         S            ",
            "                                                                              X                                                               X                                                         X            ",
            "                                                 XXXX    XXXX                 X                                                               X                                        XXXX             X            ",
            "                                                                              X                                                               X                                                         X    S       ",
            "                                                                              X                                                               X                                                 XXXXX   X    X       ",
            "                           XXXX                                               X                                                               X                                                     X   X    X       ",
            "                     XXXX                                         XXXXXXXXXXXXF                                                               X                                                     X   X    X       ",
            "XXXXXXXXXXXXXXXXXXXXX                                                                                                                         X                                                     X        X       ",
            "XFFFFFFFFFFFFFFFFFFFX                                                                                                                         X                                                     X        X       ",
            "XFFFFFFFFFFFFFFFFFFFX                                                                                                                         X                                                     X        X       ",
            "XFFFFFFFFFFFFFFFFFFFX                                                                                                                         X                           XXX                       X   XX   X       ",
            "XFFFFFFFFFFFFFFFFFFFX                                                                                                                         X                                                     X    X   X       ",
            "XFFFFFFFFFFFFFFFFFFFX                                                                                                                         XXXXXX                                                X    XXXXX       "
        ]
    elif selected_level == '7':
        #LEVEL 7
        level = [
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXXXXXXXXXX                             X                                                       ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX          D            X                X                                                       ",
            "                                                                                                                    X          D            X                X                                                       ",
            "                                                                                                                    FBXXXXXXXXXXX           X                X                                                       ",
            "                                                                                                                    FFX  XFFFFFFX           X                X                                                       ",
            "                                                                                  H                                 XFX  XFFFFFFX           X                X                                                       ",
            "                                                                                  H                                 XFX  XFFFFFFX           X                XXXXXXXXXXXXXX                                          ",
            "                                                                                  H                                 XXX  XFFFFFFX           D                                                                        ",
            "                                                                      S           H                                   X  XFFFFFFX           D                                           SSSSSSSSSSSSSSSSSSSSSSSSSS   ",
            "                                                                      X           H              SM     XXXXX            XFFFFFFFSSSSEEESSSSX     SSSSSSS    XXXXXX  XX  XXXXXXXXXXXXX  XFFFFFFFFFFFFFFFFFFFFFFFFF   ",
            "                                                                      X   S       H            XXXXX    XFFFX            XFFFFFFFFFFFXXXFFFFXXXXXXFFFFFFF    XFFFFFSSFFSSFFFFFFFFFFFFX  XFFFFFFFFFFFFFFFFFFFFFXXX    ",
            "                                                                      X   XXXXX   H            XFFFFSSSSFFFFX      XXXXXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFSSSSFFFFFFFFFFFFFFFFFFFFFFFFX  XFFFFFFFFFFFFFFFFFFFFX       ",
            "                                                                      X   XFFFFSSSSSSSSSSSSSSSSFFFFFFFFFFFFFFSSSSSSFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX  XFFFFFFFFFFFFFFFFFFFX        ",
            "                                                                      X   SFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX  XFFFFFFFFFFFFFFFFXXX         ",
            "XXXXXXXXXXXXXXXXXX                                                        XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX  XFFFFFFFFFFFFFFFX            ",
            "FFFFFFFFFFFFFFFFFF                                                        XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX  XXXXXXXXXXXXXXXX             ",
            "FFFFFFFFFFFFFFFFFF                                                        XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXX                              X",
            "FFFFFFFFFFFFFFFFFF                                                   SS  XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                X",
            "FFFFFFFFFFFFFFFFFF                           X       E     E     E XXXXXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXSSEES      E       E            X",
            "FFFFFFFFFFFFFFFFFF                           XXXXXXXXXXXXXXXXXXXXXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        ]
        #LEVEL 7
        level1_alt = [
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXXXXXXXXXXX            X                X                                                       ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX          X            X                X                                                       ",
            "                                                                                                                    X          X            X                X                                                       ",
            "                                                                                                                    FXX  XXXXXXXX           X    XXXXXXXX    X                                                       ",
            "                                                                                                                    FFX  XFFFFFFX           X    XFFFFFFX    X                                                       ",
            "                                                                                                                    XFX  XFFFFFFX           X    XFFFFFFX    X                      X                                ",
            "                                                                                                                    XFX  XFFFFFFX           X    XFFFFFFX    XXXXXXXXXXXXXX         X                                ",
            "                                                                                                                    XXX  XFFFFFFX           X    XFFFFFFX                           X                                ",
            "                                                                                                                      X  XFFFFFFX           X    XFFFFFFX                           X                                ",
            "                                                                                                                         XFFFFFFX           X    XFFFFFFX                XXXXXXXXXXXX                                ",
            "                                                                                                                         XFFFFFFX           XXXXXXFFFFFFX                XFFFFFFFFFFF                                ",
            "                                                                                      XXXXX                       XXXXXXXXFFFFFFX           XFFFFFFFFFFFX                XFFFFFFFFFFF                                ",
            "                                                                                      XFFFX                        XFFFFFFFFFFFFX           XFFFFFFFFFFFX                XFFFFFFFFFFF                                ",
            "                                                                                      XFFFX                        XFFFFFFFFFFFFX           XFFFFFFFFFFFX                XFFFFFFFFFFF                                ",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                                                   XFFFX                        XFFFFFFFFFFFFX           XFFFFFFFFFFFX                XFFFFFFFFFFF                                ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                                  XFFFX                        XFFFFFFFFFFFFX           XFFFFFFFFFFFX                XFFFFFFFFFFF                                ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                                 XFFFX                        XFFFFFFFFFFFFX           XFFFFFFFFFFFX                XFFFFFFFFFF                                 ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXX                                               XFFFX                        XFFFFFFFFFFFFX           XFFFFFFFFFFFX                XFFFFFFFFFF                                 ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                               XFFFX                        XFFFFFFFFFFFFX           XFFFFFFFFFFFX                XFFFFFFFFFF                                 ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF                                               XFFFX                        XFFFFFFFFFFFFX           XFFFFFFFFFFFX                XFFFFFFFF                                   "
        ]
    elif selected_level == '5':
        #LEVEL 5
        level = [
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                HH                                   ",
            "                                                                                                                                              XXX                               HH                                   ",
            "                                                                                                                                       XXX                                      HH                                   ",
            "                                                                                                                                 XXX                                        X                                        ",
            "                                             XXXX                                                                          XXX                             XX          X            X    X                           ",
            "XXXXXXXXXXXXXXXX    XXXX     XXXX    XXXX                                              XXXX  XXXX   XXXX    XXXX                                                                                                     ",
            "FFFFFFFFFFFFFFFX                                               XXXX           XXXXX                                                                                                                                  ",
            "FFFFFFFFFFFFFFFX                                                      XXXX                                                                                                                                           ",
            "FFFFFFFFFFFFFFFX                                                                                                                                                                            X                        ",
            "FFFFFFFFFFFFFFFX                                                                                                                                                                                X       E          X ",
            "FFFFFFFFFFFFFFFX                                                                                                                                                                                XXXXXXXXXXXXXXXXXXXX                 M"
        ]
        #LEVEL 5
        level1_alt = [
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                 XXX                                        X                                        ",
            "                                             XXXX                                                                   XXX    XXX                             XX    XX                 X    X                           ",
            "XXXXXXXXXXXXXXXX    XXXX     XXXX                     XXXX                             XXXX         XXXX    XXXX                                     XXX                                                             ",
            "FFFFFFFFFFFFFFFX                                               XXXX             XXX                                                                                                                                  ",
            "FFFFFFFFFFFFFFFX                                                      XXXX                                                                                                                                           ",
            "FFFFFFFFFFFFFFFX                                                                                                                                                                            X                        ",
            "FFFFFFFFFFFFFFFX                                                                                                                                                                                X       E          X ",
            "FFFFFFFFFFFFFFFX                                                                                                                                                                                XXXXXXXXXXXXXXXXXXXX "
        ]
    elif selected_level == '3':
        #LEVEL 3
        level = [
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                               H                                                                                                     ",
            "                                                                                                               H                                                                                                     ",
            "                                                                                                               H  XXXX  XXXX   XXXX   XXXX    XXXX                                                                   ",
            "                                                                                                               H                                     XXXX   XXX   XXX                                                ",
            "                                                                                                               H                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                     XXXX   XXXX                                                              XXX                                    ",
            "                                                                                               XXXX                                                                               XXX                                ",
            "                                                                                         XXXX                                                                                           XXX                          ",
            "                                                                                    XXXX                                                                                                   X                         ",
            "XXXXXXXXXXXXXXXXX             XXXXX XXXXX XXXXX       XXXXX XXXXX        XXXX  XXXX                                                                                                         X                        ",
            "FFFFFFFFFFFFFFFFX                                                                                                                                                                            X                       ",
            "FFFFFFFFFFFFFFFFX                                                                                                                                                                             XX                     ",
            "FFFFFFFFFFFFFFFFX                                                                                                                                                                                 XXXX               ",
            "FFFFFFFFFFFFFFFFX                                                                                                                                                                                       XXXXXXXXXXXX                         M "
        ]
        #LEVEL 3
        level1_alt = [
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                            XXXXX XXXX  XXXX   XXXX   XXXX    XXXX                                                                   ",
            "                                                                                                                                                            XXX   XXX                                                ",
            "                                                                                                                                                                      XXX                                            ",
            "                                                                                                                                                                         XXX                                        ",
            "                                                                                                     XXXX   XXXX                                                              XXX                                    ",
            "                                                                                               XXXX                                                                               XXX                                ",
            "                                                                                         XXXX                                                                                           XXX                          ",
            "                                                                                    XXXX                                                                                                   X                         ",
            "XXXXXXXXXXXXXXXXX XXXXX XXXXX XXXXX       XXXXX XXXXX XXXXX XXXXX  XXXX  XXXX                                                                                                               X                        ",
            "FFFFFFFFFFFFFFFFX                                                                                                                                                                            X                       ",
            "FFFFFFFFFFFFFFFFX                                                                                                                                                                             XX                     ",
            "FFFFFFFFFFFFFFFFX                                                                                                                                                                                 XXXX               ",
            "FFFFFFFFFFFFFFFFX                                                                                                                                                                                       XXXXXXXXXXX  "
        ]

    elif selected_level == '4':
        #LEVEL 4
        level = [
            "                                                                                                                                                                                                                     H",
            "                                                                                                                                                                                                                      ",
            "                                                                                                                                                                                                                     ",
            "                                                                        XXXXX   XXXX     SS   SS    SS                                                                                                                          ",
            "                                                                          X     X     XXXXXXXXXXXXXXXXXX   SSSSS                                                                                                                              ",
            "                                                                          X     X                          XXXXX                                                                                                            ",
            "                                                                          X   XXX                                 XXXX         XXXX  XXXX                                                                                              ",
            "                                                                          X     X                                                                        XXXX                                                                  ",
            "                                                                          X     X                                                                 XXXX          X     E    X                                               ",
            "                                                                          XXX   X                                                                               XXXXXXXXXXXX                                                      ",
            "                                                                                X                                                                                          X                                           ",
            "                                                                                X                                                                                          X                                           ",
            "                                                 XXXXXX                XXXXXXXXXX                                                                                          X                                                         ",
            "                XXXXX   XXXXX   XXXXX                           XXXXX                                                                                                      X                                                                   ",
            "XXXXXXXXXXXXXX                                           XXXXX                                                                                                             X                                                            ",
            "FFFFFFFFFFFFFX                                                                                                                                                             X                                          ",
            "FFFFFFFFFFFFFX                                                                                                                                                             X                                          ",
            "FFFFFFFFFFFFFX                                                                                                                                                             X                                        S   ",
            "FFFFFFFFFFFFFX                                                                                                                                                             XSSS    E       E                  SSSSSSX        ",
            "FFFFFFFFFFFFFX                                                                                                                                                             XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                     M                                            "
        ]
        #LEVEL 4
        level1_alt = [
            "                                                                                                                                                                                                                      ",
            "                                                                                                                                                                                                                      ",
            "                                                                                                                                                                                                                      ",
            "                                                                                                                                                                                                                      ",
            "                                                                                                                                                                                                                      ",
            "                                                                                                           XXXXX                                                                                                      ",
            "                                                                                                                         XXXX        XXXX                                                                             ",
            "                                                                                                                                           XXXX                                                                       ",
            "                                                                                                                                                  XXXX                                                                ",
            "                                                                                                                                                                                                                      ",
            "                                                                                                                                                                           X                                          ",
            "                                                                                                                                                                           X                                          ",
            "                                                                                                                                                                           X                                          ",
            "                XXXXX           XXXXX    XXXXX                  XXXXX                                                                                                      X                                          ",
            "XXXXXXXXXXXXXX                                           XXXXX                                                                                                             X                                          ",
            "FFFFFFFFFFFFFX                                                                                                                                                             X                                          ",
            "FFFFFFFFFFFFFX                                                                                                                                                             X                                          ",
            "FFFFFFFFFFFFFX                                                                                                                                                             X                                          ",
            "FFFFFFFFFFFFFX                                                                                                                                                             X                                          ",
            "FFFFFFFFFFFFFX                                                                                                                                                             X                                          "
        ]

    elif selected_level == '2':
        #LEVEL 2
        level = [
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                H                                                                                                                                                                                                    ",
            "                H                                                                                                                                                     X                                                ",
            "                H XXXXX XXXXX XXXXX XXXXX       XXXXX XXXXX XXXXX XXXXX                                                                                               X                                                                                             ",
            "                H X                                                    XXXXX                                                                                          X                                                      ",
            "                H X                                                          XXXXX                                S                                                   X                                                       ",
            "                H X                                                                 XXXXX  XXXXX  XXXXX  XXXXX  XXXXX XXXXX                                           X   XXX                                                                           ",
            "                H X                                                                                                                                                           XX                                        ",
            "                H X                                                                                                                                                              XX                                     ",
            "                  X                                                                                                           XXXXX  XXXX          XXXX   XXXX   XXXXXXXXX          XX                                                               ",
            "XXXXXXXXXXXXXXXXXX                                                                                                                                                                     XX                                               ",
            "FFFFFFFFFFFFFFFFFF                                                                                                                                                                      X                             ",
            "FFFFFFFFFFFFFFFFFF                                                                                                                                                                       X                              ",
            "FFFFFFFFFFFFFFFFFF                                                                                                                                                                       X                              ",
            "FFFFFFFFFFFFFFFFFF                                                                                                                                                                       X      ESS                 X     ",
            "FFFFFFFFFFFFFFFFFF                                                                                                                                                                       XXXXXXXXXXXXXXXXXXXXXXXXXXXX                    M                              "
        ]
        #LEVEL 2
        level1_alt = [
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                      X                                                ",
            "                  XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX XXXXX                                                                                               X                                                                                             ",
            "                  X                                                    XXXXX                                                                                          X                                                      ",
            "                  X                                                                                                                                                   X                                                       ",
            "                  X                                                                                                                                                   X   XXX                                                                           ",
            "                  X                                                                                                                                                           XX                                        ",
            "                  X                                                                                                                                                              XX                                     ",
            "                  X                                                                                                           XXXXX  XXXX   XXXX   XXXX   XXXX   XXXXXXXXX                                                                           ",
            "XXXXXXXXXXXXXXXXXX                                                                                                                                                                                                                      ",
            "FFFFFFFFFFFFFFFFFF                                                                                                                                                                                                    ",
            "FFFFFFFFFFFFFFFFFF                                                                                                                                                                                                     ",
            "FFFFFFFFFFFFFFFFFF                                                                                                                                                                                                     ",
            "FFFFFFFFFFFFFFFFFF                                                                                                                                                                                                   ",
            "FFFFFFFFFFFFFFFFFF                                                                                                                                                                                                    "
        ]

    elif selected_level == '10':
        #LEVEL 10
        level = [
            "                                                                                                                                               D                                                                     ",
            "                                                                                                                                               D                                                                     ",
            "                                                                                                                                               D                                                                     ",
            "                                                                                                                                               D                                                                     ",
            "                                                                                                                                               D                                                                     ",
            "                                                                                                                     X                         D                                                                     ",
            "                                                                                                                     X                         D                                                                     ",
            "                                                                                                                     X                         D             H                                                       ",
            "                                                                                                                     X                         D             H               S                                        ",
            "                                                                                                                     X                         D             H               X                                        ",
            "                                                                                                                     X                         D             H               X                                        ",
            "                                                                X           X   S          S            S            X       X     X     B     D             H               X                                                  ",
            "             M                        XX            XX                          XXXX       X  E EEE E   X   XXX      X                         D             H               X                                                                 ",
            "XXXXXXXXXXXXXXXXXX     XXX                                                                  XXXXXXXXXXXX                                       D   SSS       H           S   X                                                                               ",
            "FFFFFFFFFFFFFFFFFX                                                                                                S                            DXXXXXXXXXX               X   X                                                      ",
            "FFFFFFFFFFFFFFFFFX                                                                                                XXXXXXX                      D                         X                                                     ",
            "FFFFFFFFFFFFFFFFFX                                                                                                                             D                         X                                              ",
            "FFFFFFFFFFFFFFFFFX                                                                                                                             D                         X                                              ",
            "FFFFFFFFFFFFFFFFFX                                                                                                                             D                         X   XXXXXXXX                                           ",
            "FFFFFFFFFFFFFFFFFX                                                                                                                             D                         X              XXXXXXXXXXXXXXXXXXXXXX                                       "
        ]
        level1_alt = [
            "                                                                                                                                               X                                                                     ",
            "                                                                                                                                               X                                                                     ",
            "                                                                                                                                               X                                                                     ",
            "                                                                                                                                               X                                                                     ",
            "                                                                                                                                               X                                                                     ",
            "                                                                                                                                               X                                                                     ",
            "                                                                                                                        S                      X                                                                     ",
            "                                                                                                                        X                      X                                                                     ",
            "                                                                                                      X                 X                      X                                                                      ",
            "                                                                                                      X                 X                      X                             X                                        ",
            "                                                                                                      X                 X                      X                             X                                        ",
            "                                                                      X                X                                X                X     X                             X                                                  ",
            "             M                               XX            X                                                            X                      X                 XX     XX   X                                                                 ",
            "XXXXXXXXXXXXXXXXXX             XXX                                                                                      X                      X                         X   X                                                                               ",
            "FFFFFFFFFFFFFFFFFX                                                                                                      X                      X                         X   X                                                      ",
            "FFFFFFFFFFFFFFFFFX                                                                                                                             X                         X   X                                                 ",
            "FFFFFFFFFFFFFFFFFX                                                                                                                             X                         X                                              ",
            "FFFFFFFFFFFFFFFFFX                                                                                                                             X                         X                                              ",
            "FFFFFFFFFFFFFFFFFX                                                                                                                             X                         X   XXXXXXXX                                           ",
            "FFFFFFFFFFFFFFFFFX                                                                                                                             X                         X              XXXXXXXXXXXXXXXXXXXXXX                                       "
        ]

    elif selected_level == '11':
        #LEVEL 11
        level = [
            "                                      S                                                                                                                                                                              ",
            "                                      X                                                                                                                                                                              ",
            "                                      X                                                                                                                                                                              ",
            "                                   S  X                                                     XXXX                                                                                                                     ",
            "                                   X  X                                                 H           S                                                                                                                ",
            "                  S                X  X                                                 H           X E X                                                                                                            ",
            "                  X                X  X                                                 H            XXX                                                                                                             ",
            "                      S            X  X                                                 H                    S                         S                                                                             ",
            "                      X            X                                                    H                    X E X                     X   S                                                                         ",
            "                  S                X                                                    H   S                 XXX                          X                                                                         ",
            "                  X   S            X                                              S         X                                          S   X   S                                                                     ",
            "                      X            X            X           X                     X                                  S                 X     XXXXX           X                                                       ",
            "                  S     S          X                                    X         X                                  X E X             X   S                             X                                           ",
            "                  X     X          X                                                                                  XXX                  X                                                                         ",
            "XXXXXXXXXXXXXXXXXXX     X  X                                                SS                                                             X                                         X                               ",
            "FFFFFFFFFFFFFFFFFFX     X  X                                                XXX                                             S              X                                                                         ",
            "FFFFFFFFFFFFFFFFFFX        X                                                                                                XS  S ES  S S SX                                             S                           ",
            "FFFFFFFFFFFFFFFFFFX                                                                                                          XXXXXXXXXXXXXX                                              XXX                         ",
            "FFFFFFFFFFFFFFFFFFX                                                                                                                                                                         XXXXXXXXXXXXXXXXXXXXXXXX            M",
            "FFFFFFFFFFFFFFFFFFXSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
        ]
        level1_alt = [
            "                               S      S                                                                                                                                                                              ",
            "                               X      X                                               S                                                                                                                              ",
            "                               X      X                                               X                                                                                                                              ",
            "                               X      X                                               X  X                                                                                                                           ",
            "                               X      X                                               X  X                                                                                                                           ",
            "                               X      X                                               X  X                                                                                                                           ",
            "                               X      X                                               X                                                                                                                              ",
            "                               X      X                                                                                                                                                                              ",
            "                               X                                                                                                                                                                                     ",
            "                               X                                                                                                                                                                                     ",
            "                               X                                                                                                                                                                                     ",
            "                                        XXX           X           X                                                                                    X           X                                                 ",
            "                                                                        X              XXX                                                                                                                           ",
            "                                                                                                                                                                               X                                     ",
            "XXXXXXXXXXXXXXXXXXX          XXXX                                                                                                                                                                                    ",
            "FFFFFFFFFFFFFFFFFFX                                                                X                                                                                                                                 ",
            "FFFFFFFFFFFFFFFFFFX                                                                                                                                                                                                  ",
            "FFFFFFFFFFFFFFFFFFX                                                                                                                                                                                                  ",
            "FFFFFFFFFFFFFFFFFFX                                                                                                                                                                         XXXXXXXXXXXXXXXXXXXXXXXX ",
            "FFFFFFFFFFFFFFFFFFXSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
        ]

    elif selected_level == '9':
        #LEVEL 9
        level = [
            "                                                      X                                      X                                                                X                                                        ",
            "                                                      X                                      X                                                                X           H                                              ",
            "                                                      X                                      X                                                                X           H                                               ",
            "                                                      X                   XXXX    XXXXXXX    X                                                                X           H  H                                                    ",
            "                                                      X                      X          X    X                                                                X     S     H  H                                               ",
            "                                                      X                      X          X    X                                                                X     XEX      H                                               ",
            "                                                      X                      X          X    X                                                       S S S    X     XXX         H                                                 ",
            "                                                      X                      X          X    X                                                 SS  SXXXXXXXXXXX                 H                                                         ",
            "                                                      X         S            X          X    X                                            SS  XXXXXX                            H X                                             ",
            "                                                      D         X      SS    XSSSS      X                                             SS XXXXX                                    XSSSS                                             ",
            "                                                      D         X  XXXXXXXXXXXXXXX      X           XSSS   SSSEESS SSEESS SSEESS SS  XXXX                                         XXXXX                                                                         ",
            "                                                      D         X                       X    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                                             X                                                                              ",
            "                                                      D         X                       X    X                                                                                    X                                       ",
            "        M      SS  SSE SS  SSE SS  SSE SS  SSE        D         X                       X    X                                                                                    X                                     ",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXBXXXXXXXXXXXX                                                                                                                 X                                                                                            ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX         X                                                                                                                                                    ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX         X                                                                                                                                                     ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX         X                                                                                                                 S S                                 ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                                                                                                           XEX                                   ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                                                                                                           XXXXXXXXXXXXXXXXXXXXXXXXXXXX                                   "
        ]
        level1_alt = [
            "                                                      X                                      X                                                                X                X  X                                    ",
            "                                                      X                                      X                                                                X                X  X                                      ",
            "                                                      X                                      X                                                                X  S             X  X                                       ",
            "                                                      X                   XXXX    XXXXXXX    X                                                                X  X             X  X                                               ",
            "                                                      X                           X     X    X                                                                X  X             X  X                                          ",
            "                                                      X                           X     X    X                                                                   X             X  X                                          ",
            "                                                      X      X                    X     X    X                                                                   X             X  X                                               ",
            "                                                      X      X                    X     X    X                                                      XXXXXXXXXXX  X             X  X                                                       ",
            "                                                      X      X  S                 X     X    X                                                                   X             X  X                                             ",
            "                                                      X      X  X                 X     X                                                                                      X  X                                                 ",
            "                                                      X      X  X            XXXXXX     X                                                                                      X  X                                                                             ",
            "                                                      X      X  X                       X                                                                                      X  X                                                                              ",
            "                                                      X      X  X                       X                                                                                      X  X                                       ",
            "                                                      X      X  X                                                                                                              X  X                                     ",
            "XXXXXXXXXXXXX                                         XXXXXXXX  X                                                                                                              X  X                                                                                            ",
            "FFFFFFFFFFFFF                                         FFFFFFFX  X                                                                                                              X                                     ",
            "FFFFFFFFFFFFF                                         FFFFFFFX  X                                                                                                              X                                      ",
            "FFFFFFFFFFFFF                                         FFFFFFFX  X                                                                                                              X                                      ",
            "FFFFFFFFFFFFF                                         FFFFFFFX                                                                                                                 X                                        ",
            "FFFFFFFFFFFFF                                         FFFFFFFX                                                                                                                            XXXXXXXXXXXXXXXXXXXX                                   "
        ]

    elif selected_level == '8':
        #LEVEL 8
        level = [
            "                                                                                                                                                                                                                      ",
            "                                                                                                                                                                                                                           ",
            "                                                                                                                                                                                                                                   ",
            "                                                                                                                                                                                                                         ",
            "                                                                                                                                                                                                                         ",
            "                                                                                                                                                                                                                        ",
            "                                                                                                                                                                       X      X                                              ",
            "                                                                                                                                                        XX      XX                                                          ",
            "                                                                                                                              XXX      XXX      XXX                                                                              ",
            "                                                                                                                         XXX                                                         X                                      ",
            "                                                                                                                   XXX                                                                                                         ",
            "                                                                                                               SSS                                                                                                       ",
            "              S    S    S                    S  S   S    S   S                                           XXX   XXX                                                                                                                       ",
            "              XS  SXS  SX   SS   S  SS  SS   XE X ESXSE SXSESX  M                                XXX                                                                                        X                                                                ",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      XXX      XXX      XXX                                                                                                                                                                                                   ",
            "FFFFFFFFFFFFFFX                                                                                                                                                                                                        ",
            "FFFFFFFFFFFFFFX                                                                                                                                                                                                                          ",
            "FFFFFFFFFFFFFFX                                                                                                                                                                                                        ",
            "FFFFFFFFFFFFFFX                                                                                                                                                                                                       ",
            "FFFFFFFFFFFFFFX                                                                                                                                                                               XXXXXXXXXXXXXXXXX                 H"
        ]
        level1_alt = [
            "                                                        X                                                                                                                                                             ",
            "                                                        X          XXX                               XX                                                                                                                    ",
            "                                                        X  X  XX         XX   XX   XX     XX    XX                                                                                                                                 ",
            "                                                        X  X                                              XX                                                                                                             ",
            "                                                           X                                                   XXX                                                                                                       ",
            "                                                                                                                     XXX                                                                                                ",
            "                                                       XXX                                                                XXX                                                                                                ",
            "                                                 XXX                                                                                    X                                                                                   ",
            "                             X             XXX                                                                                          X                                                                                        ",
            "                             X       XXX                                                                                                X                                                                                   ",
            "                             X  XXX                                                                                                XXX  X                                                                                      ",
            "                                X                                                                                                    X  X                                                                                ",
            "                                                                                                                                     X  X                                                                                                ",
            "                                                                                                                                     X                                                                                                                       ",
            "XXXXXXXXXXXXXXX                                                                                                                      X                                                                                                                                                         ",
            "FFFFFFFFFFFFFFX                                                                                                                      X                                                                                 ",
            "FFFFFFFFFFFFFFX                                                                                                                      X  XXXX     XX     XX    X     X    X     X     XX                                                  ",
            "FFFFFFFFFFFFFFX                                                                                                                      X                                                    X                            ",
            "FFFFFFFFFFFFFFX                                                                                                                                                                                                       ",
            "FFFFFFFFFFFFFFX                                                                                                                                                                               XXXXXXXXXXXXXXXXX                 H"
        ]

    elif selected_level == '12':
        #LEVEL 12
        level = [
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
            "      FFF                                                                                                                                                                                                           X   ",
            "       F                                                                                                                                                                                                            X ",
            "       F                                                                                                                                                                                                            X ",
            "                                                                                                                                 X                                                                                  X",
            "                                                                                                                                 X                                                                                  X",
            "                S S  S  S                    S S S             S   S S               S   S               S                   S                                 S                                                    X  ",
            "X         S SSS X XS XS X SS SS SS  SSS S SS X X X   SS SS SS  X   X X  S     S  S   X   X  S    S    S  X   S  S    S    S  X      SSS      S   S   S         X                                                    X                             ",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXXXXXX XXX XXX XXX XXX XXXFXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                                                                                       X XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                                                                                       X XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX        S         S         S         S         S         S         S         S         S         S    X XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF                                                                                 ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX        F    S    F         F    S    F         F    S    F         F    S    F         F    S    F    X XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF                                                                                   ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX       SF    F    FS       SF    F    FS       SF    F    FS       SF    F    FS       SF    F    FS   X XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF                                                                                    ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX     SSFFS  SFS  SFFS    SSFFS  SFS  SFFS    SSFFS  SFS  SFFS    SSFFS  SFS  SFFS    SSFFS  SFS  SFFS  X XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                                                                                                                              ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX SSSSFFFFFSSFFFSSFFFSSSSSFFFFFSSFFFSSFFFSSSSSFFFFFSSFFFSSFFFSSSSSFFFFFSSFFFSSFFFSSSSSFFFFFSSFFFSSFFFS  X                                         X                                                                                            ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                         X  ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                    MH"
        ]
        level1_alt = [
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "HM                                                                                                                                                                                                                   ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     "
        ]





    #recreate the level with every type of block required in the list
    for t in range(len(level)):
        for i in range(len(level[t])):
            if level[t][i] == 'X':
                blocks.append("block{0}".format(100*t + i))
                blocks[number] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                number += 1
            elif level[t][i] == 'H':
                hooks.append("hook{0}".format(100*t + i))
                hooks[number4] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                number4 += 1
            elif level[t][i] == 'M':
                movers[str(number3)] = ["mover" + str(100 * t + i),0,0,False,False,shattered,finalpos,hitbox,drawn]
                movers[str(number3)][6] = (i * tilesize, t * tilesize)
                movers[str(number3)][0] = Rect ((i * tilesize, t * tilesize),(tilesize,tilesize))
                number3 += 1
            elif level[t][i] == 'D':
                blocks.append("block{0}".format(100*t + i))
                blocks[number] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                number += 1
            elif level[t][i] == 'B':
                blocks.append("block{0}".format(100*t + i))
                blocks[number] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                number += 1
            elif level[t][i] == 'E':
                enemies[str(number6)] = ["enemy" + str(100 * t + i),mxvel,actx,alive,skele_image]
                enemies[str(number6)][0] = Actor(enemies[str(number6)][4][0], (i * tilesize + enemies[str(number6)][2], t * tilesize))
                number6 += 1
            elif level[t][i] == 'S':
                saws.append("saw{0}".format(100*t + i))
                saws[number7] = Actor('saw', (i * tilesize + objx + 16, t * tilesize + 22))
                number7 += 1
            elif level[t][i] == 'F':
                fillers.append("filler{0}".format(100*t + i))
                fillers[number8] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                number8 += 1

    #underworld gimmick
    if selected_level == '12':
        dimension = False
        for h in range(kills):
            enemies[str(number6)] = ["enemy" + str(100 * h + 996),mxvel,actx,alive,skele_image]
            enemies[str(number6)][0] = Actor(enemies[str(number6)][4][0], ((h+20) * tilesize*2 + enemies[str(number6)][2], 9 * tilesize))
            number6 += 1

    #initialising blocks for level 2
    for v in range(len(level1_alt)): #row
            for q in range(len(level1_alt[v])): #column
                #if there's a block in the lizt
                if level1_alt[v][q] == 'X':

                    #giving lizt item a name
                    blocks2.append("block{0}".format(100*v + q))
                    #assign this lizt item as a rectangle in position relative to q and v
                    blocks2[number2] = Rect ((q * tilesize + objx, v * tilesize),(tilesize,tilesize))
                    #next block item
                    number2 += 1
                elif level1_alt[v][q] == 'F':
                    fillers2.append("filler{0}".format(100*v + q))
                    fillers2[number9] = Rect ((i * tilesize + objx, t * tilesize),(tilesize,tilesize))
                    number9 += 1

    #stop generating level and put player into level
    title = False
    dead2 = False

#scroll blocks right if the player goes too far to the left
def scroll_right():
    global objx, xvel, xveldiff, actx, mxvel, terminalx, selected_level
    if selected_level == '9':
        objx -= 1
        sprite.x -= 1
        portal.x -= 1
        for e in enemies:
            enemies[str(e)][2] -= 1
    elif selected_level == '5':
        objx -= 1.5
        sprite.x -= 1.5
        portal.x -= 1.5
        for e in enemies:
            enemies[str(e)][2] -= 1.5
    else:
        if not xcollidecheck(-(xvel+xveldiff)) and not xcollidecheck2(-(xvel+xveldiff)):
            objx -= xvel
            portal.x -= xvel
            for e in enemies:
                enemies[str(e)][2] -= xvel
        if xvel > -terminalx:
            xvel -= 0.25
            xveldiff = -0.25

#first stage of death, when player immediately registers a death, this is for animation and sound
def death():
    global title, objx, actx, skele_walk, dead, soundcondition
    dead = True
    if dead and soundcondition == 'On':
        sounds.deathsound.play()
    clock.schedule_unique(death2,0.5)

#second stage of death, for the black screen and reset
def death2():
    global title, objx, actx, skele_walk, dead, dimension, level_selector, dead2
    global title, objx, actx, skele_walk, dead, dimension, level_selector, dead2, level, numbero2, enemies, score, dead
    sprite.x = 300
    sprite.y = 300
    dead = False
    title = True
    dead2 = True
    if score > 0:
        score -= 1000
    sprite.x = 300
    sprite.y = 300
    objx = 0
    actx = 0
    if selected_level != '12':
        dimension = True
    else:
        dimension = False
    numbero2 = 0
    portal.x = 6500
    portal.y = 500

    for e in enemies:
        enemies[str(e)][3] = True
        enemies[str(e)][4] = skele_walk
        enemies[str(e)][0].image = 'skele1'
        enemies[str(e)][2] = 0
        enemies[str(e)][1] = 1
        for t in range (len(level)):
            for i in range (len(level[t])):
                if level[t][i] == 'E':
                    enemies[str(e)][0] = Actor(enemies[str(e)][4][0], (i * tilesize + enemies[str(e)][2], t * tilesize - tilesize + 13))
    for m in movers:
        for t in range (len(level)):
            for i in range (len(level[t])):
                if level[t][i] == 'M':
                    movers[str(m)][6] = (i * tilesize, t * tilesize)
    clock.schedule_unique(death3,1)

#final stage, put player back into level
def death3():
    global title, objx, actx, skele_walk, dead, dimension, level_selector, dead2, level, numbero2, enemies, score, dead
    title = False
    dead2 = False
    create_level()



#move the crate (ignore variable names I didn't know what to call it)
def movermove():
    global down, moverxvel, moveryvel, release, released, shattered, poo, tilesize, objx, opened
    if not title and not dead and not dead2:
        for m in movers:
                    #dragging the crate
                    if down:
                        if movers[str(m)][0].collidepoint(mousepos):
                            poo = list(movers[str(m)][6])
                            poo[0] = mousepos[0]
                            poo[1] = mousepos[1]
                            movers[str(m)][6] = tuple(poo)

                    #detect if crate falls onto ground, snap it to the grid by rounding it to the tilesize
                    elif movercollidecheck(movers[str(m)][0]):
                        movers[str(m)][3] = False

                        poo = list(movers[str(m)][6])
                        poo[0] = tilesize*round((movers[str(m)][0].left - objx)/tilesize)
                        poo[1] = tilesize*round(movers[str(m)][0].top/tilesize)
                        movers[str(m)][6] = tuple(poo)


                    #detect if the player let go of the crate
                    if movers[str(m)][3]:
                        poo = list(movers[str(m)][6])
                        poo[0] += movers[str(m)][1]
                        poo[1] -= movers[str(m)][2]
                        movers[str(m)][6] = tuple(poo)
                        if moverxvel > 0:
                            movers[str(m)][1] -= 0.1

                        movers[str(m)][2] -= 0.5

                    #open door if crate is placed on button
                    if not movers[str(m)][3]:

                        for t in range(len(level)):
                            for i in range(len(level[t])):
                                if level[t][i] == 'B':
                                    if i * tilesize + objx == movers[str(m)][6][0] + objx and t * tilesize == movers[str(m)][6][1] + 32:
                                        opened = True
                                        break
                                    else:
                                        opened = False







#move the player
def move():
    global selected_level, costume_death, dead, terminalx, tester,costume_hang, numbero, attack, costume_attack, costume_slide, costume_fall, costume_jump, left, costume_images, costume_idle, costume_run, holding, number5, lizt, gravity, ycollide, yvel, jumping, falling, slidingright, slidingleft, walljumpleft, walljumpright, xvel, xvel2, runright, runleft, first, sinx, mousepos, angle, xveldiff, yveldiff, trajectory, displacement, rope, ropexveldiff, ropeyveldiff, ropeyvel, ropexvel, center, center2, swing, sprint, crouch
    if not dead:
        #gravity and falling
        if not ycollidecheck(gravity) and not jumping:
            for h in hooks:
                if not sprite.colliderect(h):
                    falling = True
                    holding = False
                elif not dimension:
                    falling = False
                    holding = True
                    break
            if falling:
                sprite.y += gravity
                yveldiff = gravity
                if gravity < 20:
                    gravity += 0.5

        falling = False
        if jumping and not ycollidecheck(-yvel) and not ycollidecheck2(-yvel) and not rope:
            sprite.y -= yvel
            yvel -= 0.5
        elif jumping and ycollidecheck(-yvel):
            jumping = False
            yvel = 8.5
        elif jumping and ycollidecheck2(-yvel):
            yvel = 0

        #going right
        if (keyboard.right) and not xcollidecheck(xvel+xveldiff+2) and not walljumpright and not (keyboard.left) and not walljumpleft and not rope:
            #if xcollidecheck2(xvel+xveldiff-2):
                #xvel = 0
            if xvel < 0:
                xvel = 0
            if sprite.x > 594 and xvel > 0 and selected_level != '9' and selected_level != '5':
                scroll_left()
            elif sprite.x > 594 and xvel > 0:
                sprite.x += xvel
                if xvel < terminalx:
                    xvel += 0.25
                    xveldiff = 0.25
            else:

                sprite.x += xvel
                if xvel < terminalx:
                    xvel += 0.25
                    xveldiff = 0.25

        #stop velocity if player stops
        if not (keyboard.right) and not (keyboard.left) and not walljumpleft and not walljumpright and not rope and not swing:
            xvel = 0
            """if xvel > 0.75:
                xvel -= 0.5
            elif xvel < -0.75:
                xvel += 0.5
            else:
                xvel = 0
            sprite.x += xvel"""
            #blocked out code is for momentum after you stop

        #wall jump right
        if walljumpright and not xcollidecheck(xvel+xveldiff+2):
            if sprite.x > 594 and selected_level != '9' and selected_level != '5':
                scroll_left()
            elif sprite.x > 594 and xvel > 0:
                sprite.x += xvel
                if xvel < terminalx:
                    xvel += 0.25
                    xveldiff = 0.25
            else:
                if first:
                    xvel = 5
                    first = False
                elif (keyboard.left):
                    xvel -= 0.25
                    xveldiff = -0.25
                sprite.x += xvel


        #going left
        if (keyboard.left) and not xcollidecheck2(xvel+xveldiff-2) and not walljumpleft and not (keyboard.right) and not walljumpright and not rope:
            #if xcollidecheck(xvel+xveldiff+2):
                #xvel = 0
            if xvel > 0:
                xvel = 0
            if sprite.x < 300 and xvel < 0 and selected_level != '9' and selected_level != '5':
                scroll_right()
            elif sprite.x < 300 and xvel < 0:
                sprite.x += xvel
                if xvel > -terminalx:
                    xvel -= 0.25
                    xveldiff = -0.25
            else:

                sprite.x += xvel
                if xvel > -terminalx:
                    xvel -= 0.25
                    xveldiff = -0.25


        #wall jump left
        if walljumpleft and not xcollidecheck2(xvel+xveldiff-2):
            if sprite.x < 300 and selected_level != '9' and selected_level != '5':
                scroll_right()
            elif sprite.x < 300 and xvel < 0:
                sprite.x += xvel
                if xvel > -terminalx:
                    xvel -= 0.25
                    xveldiff = -0.25
            else:
                if first:
                    xvel = -5
                    first = False
                elif (keyboard.right):
                    xvel += 0.25
                    xveldiff = 0.25

                sprite.x += xvel

        #detect which direction the player is going for animation
        if xvel < 0:
            left = True
        elif xvel > 0:
            left = False

        #ladders
        for h in hooks:
            if jumping and (keyboard.up) and sprite.colliderect(h) and not dimension:
                jumping = False
                falling = False
                holding = True
                break


        for h in hooks:
            if sprite.colliderect(h) and not dimension:
                if (keyboard.up) or (keyboard.down):
                    tester = True
                break
            else:
                tester = False



        if (keyboard.up) and not jumping and ycollidecheck(gravity) and not walljumpright and not walljumpleft and not rope:
            for h in hooks:
                if sprite.colliderect(h) and not dimension:
                    jumping = False
                    falling = False
                    holding = True
                    break
                elif not sprite.colliderect(h):
                    if soundcondition == "On":
                        sounds.jumpsound.play()
                    jumping = True



        if (keyboard.up):
            for h in hooks:
                if sprite.colliderect(h) and not dimension:
                    holding = True
                    sprite.y -= 3
                    yvel = -10
                    break
                else:
                    holding = False


        if (keyboard.down):
            for h in hooks:
                if sprite.colliderect(h) and not dimension:
                    holding = True
                    sprite.y += 3
                    yvel = -10
                    break
                else:
                    holding = False



        #wall jump
        if (keyboard.up) and slidingright and not ycollidecheck(gravity):
            walljumpleft = True
            first = True

            clock.schedule_unique(stop, 0.5)
            yvel = 8.5
            jumping = True
            if soundcondition == "On":
                sounds.jumpsound.play()
            slidingright = False

        #wall jump
        if (keyboard.up) and slidingleft and not ycollidecheck(gravity):
            walljumpright = True
            first = True

            clock.schedule_unique(stop, 0.5)
            yvel = 8.5
            jumping = True
            if soundcondition == "On":
                sounds.jumpsound.play()
            slidingleft = False

        #kill player if they fall in void
        if sprite.top > 1000 and not dead:
            death()


        #sliding down walls
        if yvel < -2 and xcollidecheck(xvel+xveldiff+2) and (keyboard.right):
            slidingright = True

        if yvel < -2 and xcollidecheck2(xvel+xveldiff-2) and (keyboard.left):
            slidingleft = True

        #stop sliding
        if (walljumpright and xcollidecheck(xvel+xveldiff+2)) or (walljumpleft and xcollidecheck2(xvel+xveldiff-2)) or ycollidecheck(gravity) or (ycollidecheck(gravity) and (slidingleft or slidingright)):
            stop()

        #stop sliding
        if slidingleft and (keyboard.right):
            slidingleft = False

        #stop sliding
        if slidingright and (keyboard.left):
            slidingright = False

    #detect condition of player, set animation accordingly
    if dead:
        costume_images = costume_death
    elif attack:
        costume_images = costume_attack
    elif holding:
        costume_images = costume_hang
    elif slidingleft:
        costume_images = costume_slide
    elif slidingright:
        costume_images = costume_slide
    elif jumping and yvel < 0:
        costume_images = costume_jump
    elif jumping and yvel >= 0:
        costume_images = costume_jump
    elif falling:
        costume_images = costume_fall
    elif xvel != 0:
        costume_images = costume_run
    else:
        costume_images = costume_idle
    """if slidingleft:
        costume.image = 'jumper-jleft'
    elif slidingright:
        costume.image = 'jumper-jright'
    elif xvel < 0:
        costume.image = 'idle1'
    elif costume.image != 'idle1' or xvel > 0:
        costume.image = 'idle1'"""


    """if swing:
        if ycollidecheck(-yvel) or ycollidecheck2(-yvel) or xcollidecheck(xvel) or xcollidecheck2(xvel):
            swing = False
        if sprite.x > 700:
            scroll_left()
        elif sprite.x < 300:
            scroll_right()
        else:
            sprite.x += xvel
        falling = True
        if xvel > 0:
            xvel -= 0.25
        elif xvel < 0:
            xvel += 0.25

    if rope:
        if ycollidecheck(gravity+1):
            yvel = 0
        jumping = False
        try:
            angle = math.degrees(math.atan((mousepos[0] - sprite.x)/(sprite.y - mousepos[1])))
        except:
            angle = 0

        if ycollidecheck(yvel) or ycollidecheck2(yvel):
            yvel = 0
        if xcollidecheck(xvel+0.5) or xcollidecheck(xvel-0.5) or xcollidecheck2(xvel+0.5) or xcollidecheck2(xvel-0.5):
            xvel = 0
            #factors to consider: initial velocity in both directions (difficult), angle at each frame (done), length of rope (ez), gravity is universal
            #ropexvel = ((math.sin(math.sin(math.sin(center/10))))/0.746)*10
            #ropeyvel = int(math.sqrt((26/(26*math.cos(center)^2)))*math.cos(center)) idk why this doesnt work good luck future me
            #ropexvel = math.sin(center/10) * 10
            #ropeyvel = math.sin(center/5) * 10
            #sprite.x += ropexvel
            #sprite.y += ropeyvel
            #center += 1
            #center2 += 1
            #pass
        if True:
            if sprite.x > 700:
                scroll_left()
            elif sprite.x < 300:
                scroll_right()

            elif mousepos[0] - sprite.x > 0:
                xvel += 0.5
            else:
                xvel -= 0.5
            sprite.x += xvel

            if mousepos[1] - sprite.y > 0:
                yvel += 0.5
            else:
                yvel -= 0.5
            sprite.y += yvel
            sprite.y -= ropeyvel
            sprite.x += ropexvel
            if angle > 0 and ropexvel > 0:
                ropexveldiff = 0.25
                ropexvel += ropexveldiff
                ropeyveldiff = -0.25
                ropeyvel += ropeyveldiff

            elif angle < 0 and ropexvel > 0:
                ropexveldiff = -0.25
                ropexvel += ropexveldiff
                ropeyveldiff = 0.25
                ropeyvel += ropeyveldiff

            elif angle > 0 and ropexvel < 0:
                ropexveldiff = 0.25
                ropexvel += ropexveldiff
                ropeyveldiff = 0.25
                ropeyvel += ropeyveldiff

            elif angle < 0 and ropexvel < 0:
                ropexveldiff = -0.25
                ropexvel += ropexveldiff
                ropeyveldiff = -0.25
                ropeyvel += ropeyveldiff
            elif ropexvel == 0:
                if costume.image == 'left':
                    ropexvel -= 1
                else:
                    ropexvel += 1"""
            #this code works more as a grappling hook if you remove the rope from front of the veldiff's and the vel's
    #kill player if they phase into a block in another realm, remove collisions for fillers because lag
    if not dead:
        if not dimension:
            number5 = 0
            if opened:
                lizt = []
                for t in range (len(level)):
                    for i in range (len(level[t])):
                        if level[t][i] == 'X':
                            lizt.append(blocks[number5])
                            number5 += 1
                        elif level[t][i] == 'B':
                            lizt.append(blocks[number5])
                            number5 += 1
                        elif level[t][i] == 'D':
                            number5 += 1
            else:
                lizt = blocks
            for b in lizt:

                    if sprite.colliderect(b) and not dead:
                        death()
            #for f in fillers:
                #if sprite.colliderect(f) and not dead:
                    #death()
        else:
            for k in blocks2:

                    if sprite.colliderect(k) and not dead:
                        death()
            #for f in fillers2:
                #if sprite.colliderect(f) and not dead:
                    #death()






"""def on_key_down(LCTRL):
    global sprint
    sprint = True

def on_key_up(LCTRL):
    global sprint
    sprint = False
 or (walljumpright and (keyboard.left)) or (walljumpleft and (keyboard.right))"""


#detect if the crate collides with blocks
def movercollidecheck(self):

    lizt = blocks
    for h in range(len(lizt)):
        if pygame.Rect.colliderect(self, lizt[h]):
        #if (self.bottom + dir > lizt[h].top and self.bottom + dir < lizt[h].bottom and self.right > lizt[h].left and self.left < lizt[h].right) or (sprite.top + dir < blocks[h].bottom and sprite.top + dir > blocks[h].top and sprite.right > blocks[h].left and sprite.left < blocks[h].right):
            return True

"""def moverxcollidecheck(self, dir):
    if dimension:
        lizt = blocks2
    else:
        lizt = blocks
    for h in range(len(lizt)):
        if (self.right + dir > lizt[h].left and self.right + dir < lizt[h].right and self.top < lizt[h].bottom and self.bottom > lizt[h].top) or (self.left + dir < lizt[h].right and self.left + dir > lizt[h].left and self.top < lizt[h].bottom and self.bottom > lizt[h].top):
            return True"""

#collide checks for every side of a block
def ycollidecheck(dir):
    global ycollide
    global blocks
    global blocks2
    global gravity, lizt, number5, level, level1_alt, totalreleased
    number5 = 0
    if dimension:
        lizt = blocks2
    elif opened and not dimension:
        lizt = []
        for t in range (len(level)):
            for i in range (len(level[t])):
                if level[t][i] == 'X':
                    lizt.append(blocks[number5])
                    number5 += 1
                elif level[t][i] == 'D':
                    number5 += 1
                elif level[t][i] == 'B':
                    lizt.append(blocks[number5])
                    number5 += 1
    else:
        lizt = blocks
    #for e in enemies:
        #if enemies[str(e)][4]:
            #totalrealeased = True
    for m in movers:
        for h in range(len(lizt)):
                if (sprite.bottom + dir > lizt[h].top and sprite.bottom + dir < lizt[h].bottom and sprite.right > lizt[h].left and sprite.left < lizt[h].right) or ((not dimension and sprite.bottom + dir > movers[str(m)][0].top and sprite.bottom + dir < movers[str(m)][0].bottom and sprite.right > movers[str(m)][0].left and sprite.left < movers[str(m)][0].right) and not down):
                    ycollide = True
                    falling = False
                    swing = False
                    gravity = 0
                    break
                else:
                    ycollide = False

    return ycollide

def ycollidecheck2(dir):
    global ycollide
    global blocks
    global gravity, lizt, number5, totalreleased
    number5 = 0
    if dimension:
        lizt = blocks2
    elif opened and not dimension:
        lizt = []
        for t in range (len(level)):
            for i in range (len(level[t])):
                if level[t][i] == 'X':
                    lizt.append(blocks[number5])
                    number5 += 1
                elif level[t][i] == 'D':
                    number5 += 1
                elif level[t][i] == 'B':
                    lizt.append(blocks[number5])
                    number5 += 1
    else:
        lizt = blocks
    #for e in enemies:
        #if enemies[str(e)][4]:
            #totalrealeased = True
    for m in movers:
        for h in range(len(lizt)):
                if (sprite.top + dir < lizt[h].bottom and sprite.top + dir > lizt[h].top and sprite.right > lizt[h].left and sprite.left < lizt[h].right) or ((not dimension and sprite.top + dir < movers[str(m)][0].bottom and sprite.top + dir > movers[str(m)][0].top and sprite.right > movers[str(m)][0].left and sprite.left < movers[str(m)][0].right) and not down):
                    ycollide = True
                    falling = False
                    swing = False
                    gravity = 0
                    break
                else:
                    ycollide = False

    return ycollide


def xcollidecheck(dir):
    global xcollide, blocks, lizt, number5, costume_images, costume_idle, blocks2, dimension, xvel, totalreleased
    number5 = 0
    if dimension:
        lizt = blocks2
    elif opened and not dimension:
        lizt = []
        for t in range (len(level)):
            for i in range (len(level[t])):
                if level[t][i] == 'X':
                    lizt.append(blocks[number5])
                    number5 += 1
                elif level[t][i] == 'D':
                    number5 += 1
                elif level[t][i] == 'B':
                    lizt.append(blocks[number5])
                    number5 += 1
    else:
        lizt = blocks
    #for e in enemies:
        #if enemies[str(e)][4]:
            #totalrealeased = True
    for m in movers:
        for h in range(len(lizt)):
                #remove xvel condition for trade off between animation and function
                if (xvel > 0) and ((sprite.right + dir > lizt[h].left and sprite.right + dir < lizt[h].right and sprite.top < lizt[h].bottom and sprite.bottom > lizt[h].top) or ((not dimension and sprite.right + dir > movers[str(m)][0].left and sprite.right + dir < movers[str(m)][0].right and sprite.top < movers[str(m)][0].bottom and sprite.bottom > movers[str(m)][0].top) and not down)):
                    xcollide = True
                    xvel = 0
                    swing = False

                    break
                else:
                    xcollide = False

    return xcollide

def xcollidecheck2(dir):
    global xcollide, blocks, lizt, number5, dimension, blocks2, costume_images, costume_idle, xvel, totalreleased
    number5 = 0
    if dimension:
        lizt = blocks2
    elif opened and not dimension:
        lizt = []
        for t in range (len(level)):
            for i in range (len(level[t])):
                if level[t][i] == 'X':
                    lizt.append(blocks[number5])
                    number5 += 1
                elif level[t][i] == 'D':
                    number5 += 1
                elif level[t][i] == 'B':
                    lizt.append(blocks[number5])
                    number5 += 1
    else:
        lizt = blocks
    #for e in enemies:
        #if enemies[str(e)][4]:
            #totalrealeased = True
    for m in movers:
        for h in range(len(lizt)):
                #remove xvel condition for trade off between animation and function
                if (xvel < 0) and ((sprite.left + dir < lizt[h].right and sprite.left + dir > lizt[h].left and sprite.top < lizt[h].bottom and sprite.bottom > lizt[h].top) or ((not dimension and sprite.left + dir < movers[str(m)][0].right and sprite.left + dir > movers[str(m)][0].left and sprite.top < movers[str(m)][0].bottom and sprite.bottom > movers[str(m)][0].top) and not down)):


                    xcollide = True
                    xvel = 0
                    swing = False
                    break
                else:
                    xcollide = False

    return xcollide

#reset wall jump related variables
def stop():
    global walljumpright, walljumpleft, slidingleft, slidingright
    slidingleft = False
    slidingright = False
    walljumpright = False
    walljumpleft = False

    counter = 0


    return slidingleft, slidingright, walljumpleft, walljumpright


def on_key_down(key):
    global credit, title, attack, dimension, groundcolour, groundcolour2, xvel, crouch, sprint

    #switch dimension
    if key == keys.SPACE and selected_level != '12':


        if not title:
            if soundcondition == "On":
                music.play_once('shiftsound')
            if dimension:
                groundcolour = 120, 120, 120
                groundcolour2 = 255, 0, 255
                dimension = False

                return
            else:
                groundcolour = 255, 255, 255
                groundcolour2 = 120, 0, 120
                dimension = True


                return
    #elif key == keys.ESCAPE:
        #if not title:
            #title = True


    #attack
    elif key == keys.LCTRL and not attack:
        attack = True
        if soundcondition == "On":
            sounds.attacksound.play()

    #full screen
    elif key == keys.F:
        screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    #exit full screen
    elif key == keys.W:
        screen.surface = pygame.display.set_mode((WIDTH, HEIGHT))

    elif key == keys.S:
        screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    #elif key == keys.K:
        #credit = True
        #title = True
def on_mouse_down(pos, button):
    global soundcondition, down, mousepos, rope, opened, title, level_selector, selected_level, totalreleased, credit, unlocked, setting, credit, objx
    if not setting:
        if not credit:
            if button == mouse.LEFT:
                if not title:
                    for m in movers:
                        if movers[str(m)][0].collidepoint(mousepos):
                            totalreleased = True
                            movers[str(m)][4] = True
                            mousepos = pos
                            down = True
                            release = False
                elif not level_selector:
                    if start.collidepoint(pos):
                        level_selector = True
                    if settings.collidepoint(pos):
                        if soundcondition == 'On':
                            soundcondition = 'Off'
                            sounds.ost2.stop()
                        else:
                            soundcondition = 'On'
                            sounds.ost2.play(-1)
                else:
                    for n in selectors:
                        if selectors[str(n)][0].collidepoint(pos) and unlocked >= eval(n):
                            selected_level = str(n)
                            title = False
                            level_selector = False
                            create_level()
                    if Menu.rect.collidepoint(pos):
                        level_selector = False
        else:
            if button == mouse.LEFT:
                if Return.rect.collidepoint(mousepos):
                    credit = False
                    title = True
                    level_selector = True

        if not title:
            if settingicon.collidepoint(pos):
                setting = True
                title = True
    else:
        if Back2LS.rect.collidepoint(pos):
            title = True
            level_selector = True
            setting = False
        if ToGame.rect.collidepoint(pos):

            title = False
            setting = False

        if Sounds.rect.collidepoint(pos):
            if soundcondition == 'On':
                soundcondition = 'Off'
                sounds.ost2.stop()
            else:
                soundcondition = 'On'
                sounds.ost2.play(-1)


def on_mouse_up(pos, button):
    global down, release, rope, swing, opened, totalreleased
    down = False
    totalreleased = False
    """if rope:
        rope = False
        swing = True"""
    for m in movers:
        if movers[str(m)][4]:
            movers[str(m)][4] = False

            movers[str(m)][3] = True


def on_mouse_move(pos, rel, buttons):
    global mousepos, moverxvel, moveryvel, poo
    mousepos = pos
    if down:
        for m in movers:

            if movers[str(m)][4]:
                poo = list(movers[str(m)][6])
                poo[0] = mousepos[0] - objx
                poo[1] = mousepos[1]
                movers[str(m)][6] = tuple(poo)
                movers[str(m)][1] = rel[0]
                movers[str(m)][2] = -1 * rel[1]

#momentum and wall jump not working :( done
#glitch where slidingleft and slidingright dont stop if you hop off a wall done
#transparency with dimensions done
#wall jump momentum physics done
#movers still need to align with rest of blocks when scrolling
#still remain sliding down wall when wall is segmented/incomplete
#need individual variables for each mover, probably create them as dictionary items so their release velocity can be independent done
#changing background done

#current to do:
#art, animation, fix movers with collisions and align them with other blocks, fix player collisions because sometimes you phase, fix rope physics, add levels, fix the lizt assignment index out of range bug, mover collision with player, mover keeps position while mouse down


#more to do: fix rope physics and the relationship between rope x and y vel and normal x and y vel, fix clipping issue, maybe get rid of sliding after you stop moving, add collisions to movers

#main bugs: clipping, movers collisions and staying in the level, revamp momentum system cuz it's buggy



#clipping bug reaaaaaaalllyy should be solved
#working on movers collision right now


#can't have more than one mover in a level

#12th August Bug Report: Everything's working. Still have the occasional clipping of the player, rope collisions and physics needs serious work


#levels
#main menu

#15th August Bug Report: fixed the occasional player clipping, every so often they get stuck on a block (xcollidecheck issue), would be nice if I could put more than one mover in a level, just need to add enemies, animations, a death process, sound effect & music, buttons that activate the doors, levels, settings, and a better home screen


#21st August Dev Log: Everything is finally coming together, add score and lives, running sounds, settings, and locked levels, you need to fix audio overlapping by converting all files to mp3 or wav, and you need to make all the levels, also sometimes there's a bug when resetting the enemies
#moving blocks
#sprint
#double jump
#wall jump done
#rope
#spikes
#crouch
#momentum done
#rain done
#settings
#particles
#music & sfx
#art
#gun
#enemies
#ideas: slow, fast, upside down, overlayed(more intertwined, everything in same place), sideways, spiral/spinning gravity, gravity inwards, gravity outwards
#lives
#black hole
#peer into the other dimension vs enter it, dimension hopping
#enemies that stay in one dimension vs enemies that can hop across them
#ice
#slide
#powerups possibly
#portals

#switching gravity in the underworld

#stationary enemies, moving enemies, flying enemies, following enemies


#wall jump switch dimension wall jump switch dimension rope swing grapple level

#things that need work: art, animations, aesthetic of the game as a whole, making it 'fun' (movement and level design), turn rects into surfaces for transparency, collisions in other dimensions

#settings button needs to be able to: change transparency of blocks in other realms, turn sounds off, return to title or level selector, and reset the character
#Dev log 28th August 2022: you need to add the settings, locked levels, the rest of the levels, and potentially mover collisions with fillers, also idk if i fixed this bug by moving the reset to death2 but sometimes player dies twice
#level ideas: transporting a mover through the whole level, basic platforming with occasional switching, 'dropper' from a wall jump, the final level as the underworld where you fight everything you've killed, jumping (between realms and platforms), jumping between ladders, 'cave',
#false collisions: death phasing into blocks, stuck inside block when going forwards and clipping down onto it
#problems: lag, dying twice sometimes, sometimes dying from false collisions

#levels to add: transport the mover, constant switching three block big jumps, switching wall jumps, using mover to help platform, credits (Hayden, Jack, Will as game testers)
#Dev log 29th August 2022: trade off: either have the collision bug where you sometimes get caught on a block with smooth collision animation, or have weird looking collision animation with the xvel checks in the xcollidechecks that solve the clipping issue

#Dev log 31st August: hide extra ladders and crates far off the level, potentially fix yvelocity of ladders, make level 5 an autoscroll

#Dev log 2nd September: finishing it up, realised I forgot running sound effect, and sliding sound effect, and portal sound effect, realised I could've done things way more efficiently: I created a class for buttons, and realised I should've had a 'state' variable that i changed rather than have a million conditions for if title, level_selector, credit, settings etc. Too late now I guess
#death animation plays twice sometimes :(

#bugs: death animation, corner death, lag, enemies clipping, everything to do with crates, wall jump hyperacceleration, animation frames missing, full screen

"""level = [
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "HM                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     ",
            "                                                                                                                                                                                                                     "
        ]
level1_alt = [
            "                                                                                                                               S                                                                                      ",
            "                                                                                                                               D            X                X                                                            ",
            "                                                                                                                               D            X                X                                                            ",
            "                                                                                                                     XBXHXXXXXXXX           X    XXXXXXXX    X                                                                          ",
            "                                                                                                                     XXXHX      X           X    X      X    X                                                              ",
            "                                                                                  H                                    XHX      X           X    X      X    X                                                               ",
            "                                                                                  H                                    XHX      X           X    X      X    X                                                              ",
            "                                                                                  H                                    XHX      X           X    X      X                                                                  ",
            "                                                                       X          H                                    XHX      X           D    X      X                                                                                ",
            "HM                                                                     X          H              S      XXXXX           HX      XSSSSEEESSSSD    X      X    XXXXX                                                                        ",
            "                                                                       X  S M     H            XXXXX    X   X            X      XXXXXXXXXXXXXXXXXX                                                                                                        ",
            "                                                                       S  XXXXX   H   XXXXX    X   X    X   X       XXXXXX                                                                                                                    ",
            "                                                                       X  X   X       X   X    X   X    X   X       X                                                                                                        ",
            "                                                                       X  S   X       X   X    X   X    X   X       X                                                                                                        ",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                                       X   X       X   X    X   X    X   X       X                                                                                                            ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                      X   X       X   X    X   X    X   X       X                                                                                                            ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                     X   X       X   X    X   X    X   X       X                                                                                                                     ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXX                              SS  X    X       X   X    X   X    X   X       X                                                                                                              ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX              E     E     E XXXXXX     XSSSSSSSX   XSSSSX   XSSSSX   X       X                                                                                                                           ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF      XXXXXXXXXXXXXXXXXXXXXX           XXXXXXXXX   XXXXXX   XXXXXX   X       X                                                                                                                                  "
        ]
level1_alt = [
            "                 XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXFFFFFFFFFFFFFFFFFFFFFFFF                               ",
            "                 XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                            X          D            X                XFFFFFFFFFFFFFFFFFFFFFF                                 ",
            "                 XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                            X          D            X                XFFFFFFFFFFFFFFFFFFFFF                                  ",
            "                 XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                            XBX HXXXXXXXX           X    XXXXXXXX    XFFFFFFFFFFFFFFFFFF                                     ",
            "                 XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                            XFX HXFFFFFFX           X    XFFFFFFX    XFFFFFFFFFFFFFFXXX                                      ",
            "                 XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX          H                                 XFX HXFFFFFFX           X    XFFFFFFX    XFFFFFFFFFFFFFX                                         ",
            "                 XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX          H                                 XFX HXFFFFFFX           X    XFFFFFFX    XXXXXXXXXXXXXX                                          ",
            "                 XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX          H                                 XXX HXFFFFFFX           X    XFFFFFFX                                                            ",
            "                 XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX          H                                   X HXFFFFFFX           D    XFFFFFFX                               SSSSSSSSSSSSSSSSSSSSSSSSSS   ",
            "HM               XFFFFFFFFFFFFFXXXXXX         FFFFFFFFFFFFFFFFFFFFFFFFFX          H              S      XXXXX           HXFFFFFFXSSSSEEESSSSD    XFFFFFFX    XXXXXX  XX  XXXXXXXXXXXXX  XXXXXXXFFFFFFFFFFFFFFFFFFF   ",
            "                 XFFFFXXXXXXXXX                FFFFFFFFFFFFFFFFFFFFFFFFX  S M     H            XXXXX    XFFFX            XFFFFFFXXXXXXXXXXXXXXXXXXFFFFFFX    XFFFFXSSXXSSXFFFFFFFFFFFX  XFFFFFFFFFFFFFFFFFFFFFXXX    ",
            "                 XXXXX                          FFFFFFFFFFFFFFFFFFFFFFFS  XXXXX   H   XXXXX    XFFFXSSSSXFFFX      XXXXXXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXSSSSXFFFFFXXFFXXFFFFFFFFFFFFX  XFFFFFFFFFFFFFFFFFFFFX       ",
            "                                                  XFFFFFFFFFFFFFFFFFFFFX  X   XSSSSSSSXFFFXSSSSXFFFXXXXXXFFFXSSSSSSXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXXXXXFFFFFFFFFFFFFFFFFFFFFFFX  XFFFFFFFFFFFFFFFFFFFX        ",
            "                                                   XFFFFFFFFFFFFFFFXXXXX  S   XXXXXXXXXFFFXXXXXXFFFFFFFFFFFFXXXXXXXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX  XFFFFFFFFFFFFFFFFXXX         ",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                XFFFFFFFFFFFFFFX       XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX  XFFFFFFFFFFFFFFFX            ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX               XFFFFFFFFFFFFFX        XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX  XFFFFFFFFFFFFFFX             ",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX               XXXXXXXXXXXXX         XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXX  XXXXXXXXXXXXXX              X",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXX                              SS  XFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX                                X",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFX      X       E     E     E XXXXXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXSSEESS     E       E            X",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF      XXXXXXXXXXXXXXXXXXXXXXFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        ]"""
