import pygame as py
import random
from math import *

#####################################################joueur#####################################################
class Joueur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spawn_coo = []
        self.finish_coo = []

        self.munition = 2   #2 est le max
        self.reload = 0.01
        self.chute = 0
        
        self.direction = 1 #0 = left , 1 = right
        self.animation = 0 #pour le déplacement

        self.bomb = [] #x, y, deltax, deltay
        self.bomb_reload = 1
        self.bomb_timer = 100
    
    def move(self):
        '''
        permet au joueur de se deplacer et de quitter
        permet au joueur de recharger son arme
        fait bouger et recharger la bombe
        fait exploser la bombe
        '''
        global game, level
        
        #gravite
        if L.active_map[int((self.y+30)/30)][int((self.x+7)/30)] == 1 or L.active_map[int((self.y+30)/30)][int((self.x+23)/30)] == 1:
            #print("touche")
            self.chute = 0
            self.y = 10*int(self.y/10)   #pour que ca s'arrete pile sur le sol
        
        else:
            self.chute += 0.14

        if L.active_map[int((self.y+30)/30)][int((self.x+20)/30)] == 2:
            self.chute = 0
        
        
        
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                #fire
                if event.key == py.K_SPACE and self.munition >= 1:
                    bullets.append([self.x + 30 if self.direction == 1 else self.x - 6, self.y + 10, self.direction, "player"])
                    self.munition -= 1
                    gun.play()
                if event.key == py.K_c and self.bomb_reload >= 1:
                    self.bomb = [self.x, self.y, -2 if self.direction == 0 else 2, 0]
                    self.bomb_reload = 0
                    self.bomb_timer = 300
                    timer.play()
                    #py.mixer.Sound.set_volume(100)
                if event.key == py.K_r:
                    game = False
                if event.key == py.K_ESCAPE:
                    game = False
                    L.level = 1000
        keys = py.key.get_pressed()
        #move
        if (keys[py.K_z] or keys[py.K_UP]) and (L.active_map[int((self.y+30)/30)][int((self.x+7)/30)] == 1 or L.active_map[int((self.y+30)/30)][int((self.x+23)/30)] == 1):
            self.chute = -3
        if (keys[py.K_z] or keys[py.K_UP]) and L.active_map[int((self.y+30)/30)][int((self.x+15)/30)] == 2 and not(L.active_map[int((self.y)/30)][int((self.x+7)/30)] == 1 or L.active_map[int((self.y)/30)][int((self.x+23)/30)] == 1):
            self.chute = -3
        
        if (keys[py.K_s] or keys[py.K_DOWN]) and L.active_map[int((self.y+30)/30)][int((self.x+15)/30)] == 2:
            self.chute = 3
        
        if (keys[py.K_q] or keys[py.K_LEFT]) and (L.active_map[int((self.y)/30)][int((self.x+5)/30)] != 1 and L.active_map[int((self.y+27)/30)][int((self.x+5)/30)] != 1):
            self.x -= 3
            self.direction = 0
        
        if (keys[py.K_d] or keys[py.K_RIGHT]) and (L.active_map[int((self.y)/30)][int((self.x+25)/30)] != 1 and L.active_map[int((self.y+29)/30)][int((self.x+25)/30)] != 1):
            self.x += 3
            self.direction = 1
        
        if L.active_map[int((self.y)/30)][int((self.x+15)/30)] == 1:
            self.chute = 0.6
        
        if not(keys[py.K_q] or keys[py.K_LEFT] or keys[py.K_d] or keys[py.K_RIGHT]):
            self.animation = 0
        else:
            self.animation += 0.1
        
        if self.animation >= 4:
            self.animation = 0

        self.y += self.chute
        
        if self.direction == 0:
            fen.blit(left_walk[int(self.animation)], (self.x, self.y))
        else:
            fen.blit(right_walk[int(self.animation)], (self.x, self.y))
        


        #fire reload
        if self.munition <= 2:
            if self.reload >= 1:
                self.munition += 1
                self.reload = 0
            self.reload += 0.02

        #bomb move
        if self.bomb != []:
            try:#la bombe peut aller trop bas à cause de la vitesse et passer sous la map
                if L.active_map[int((self.bomb[1]+5)/30)][int((self.bomb[0]+2.5)/30)] == 1:
                    while L.active_map[int((self.bomb[1])/30)][int((self.bomb[0]+2.5)/30)] == 1 and self.bomb[3] > 0:
                        self.bomb[1] -= 30
                    self.bomb[3] = -0.75 * self.bomb[3]
                    self.bomb[1] = (int(self.bomb[1]/30))*30+25

                #print("tried")
            except:
                self.bomb[3] = -0.75 * self.bomb[3]
                self.bomb[1] = 565
            if L.active_map[int((self.bomb[1])/30)][int((self.bomb[0]+2.5)/30)] == 1:
                self.bomb[3] = -0.75 * self.bomb[3]
                self.bomb[1] = (int(self.bomb[1] / 30)) * 30 + 35
            try:#la bombe peut aller trop bas à cause de la vitesse et passer sous la map
                if L.active_map[int((self.bomb[1]+2.5)/30)][int((self.bomb[0])/30)] == 1:
                    self.bomb[2] = -0.75 * self.bomb[2]
                    self.bomb[0] = (int(self.bomb[0]/30))*30+30
            except:
                self.bomb[3] = -0.75 * self.bomb[3]
                self.bomb[1] = 565
            if L.active_map[int((self.bomb[1]+2.5)/30)][int((self.bomb[0]+5)/30)] == 1:
                self.bomb[2] = -0.75 * self.bomb[2]
                self.bomb[0] = (int(self.bomb[0]/30))*30+15
            
            self.bomb[0] += self.bomb[2]
            self.bomb[1] += self.bomb[3]
            self.bomb[2] = 0.99 * self.bomb[2]
            self.bomb[3] += 0.28
            fen.blit(bomb, (self.bomb[0], self.bomb[1]))
            self.bomb_timer -= 2
            
            #explode
            if self.bomb_timer <= 0:
                new_aliens = []
                #py.mixer.timer.set_volume(0)
                boom.play()
                for a in Alien.aliens:
                    #print(sqrt((((a.x + 15)-(self.bomb[0]+2.5))**2)+(((a.y+15)-(self.bomb[1]+2.5))**2)))
                    if sqrt((((a.x + 15)-(self.bomb[0]+2.5))**2)+(((a.y+15)-(self.bomb[1]+2.5))**2)) >= 90:
                        new_aliens.append(a)
                    Alien.aliens = new_aliens
                if sqrt((((self.x + 15)-(self.bomb[0]+2.5))**2)+(((self.y+15)-(self.bomb[1]+2.5))**2)) <= 90:
                    #global game
                    game = False
                    
                

                self.bomb = []
        elif self.bomb_reload < 1:
            self.bomb_reload = round(self.bomb_reload + 0.01, 3)
        else:
            self.bomb_reload = 1


#####################################################alien#####################################################
class Alien:
    
    aliens = []
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reload = 1
        self.direction  = random.randint(0,1)
        self.skin = random.randint(0,2)


    def show():
        for mob in Alien.aliens:
            fen.blit(skin_alien[mob.direction][mob.skin], (mob.x, mob.y))


    def fire():
        for mob in Alien.aliens:
            mob.reload += 0.01
            fire = True
            direction = 0
            if mob.reload >= 1 and abs(mob.y-player.y) <= 20:
                if mob.x <= player.x:
                    direction = 1
                    for a in range(int(mob.x/30), int(player.x/30)):
                        #print(active_map[4][a])
                        if L.active_map[int(mob.y/30)][a] == 1:
                            fire = False
                else:
                    direction = 0
                    for a in range(int(player.x/30), int(mob.x/30)):
                        if L.active_map[int(mob.y/30)][a] == 1:
                            fire = False
            
                if fire:
                    a = int(player.x/30)-1
                    bullets.append([mob.x + 30 if direction == 1 else mob.x - 6, mob.y + 10, direction, "alien"])
                    #print("fire")
                    mob.direction = 0 if direction == 1 else 1
                    mob.reload = 0
                    gun.play()
                    

#####################################################level#####################################################
class Level:
    level = 0
    levels = [["maps/map_01.csv", 0], ["maps/map_02.csv", 15], ["maps/map_03.csv", 20], ["maps/map_03.csv", 30], ["maps/map_04.csv", 30]]

    def __int__(self):
        active_map = n_map(levels[Level.level])
        start_aliens = []

    def n_map(self, lien):
        with open(lien[0]) as csv:
            global start_aliens
            csv = csv.read()
            csv = csv.split("\n")
            # csv = csv.pop()
            new_map = []
            self.start_aliens = []
            # print(csv)
            for y in range(len(csv)):
                csv[y] = csv[y].split(",")
                new_map.append([])
                for x in range(len(csv[y]) - 1):
                    if int(csv[y][x]) < 9:
                        new_map[y].append(int(csv[y][x]))
                    else:
                        if int(csv[y][x]) == 10:
                            self.start_aliens.append([x * 30, y * 30])
                            new_map[y].append(0)
                        if int(csv[y][x]) == 11:
                            player.spawn_coo = [x * 30, y * 30]
                            new_map[y].append(3)
                        if int(csv[y][x]) == 12:
                            player.finish_coo = [x * 30, y * 30]
                            new_map[y].append(3)

            # print(len(new_map), len(new_map[19]))
            while len(self.start_aliens) < lien[1]:
                x = random.randint(0, 38)
                y = random.randint(0, 18)
                # print(x,y)
                if new_map[y][x] == 0 and new_map[y + 1][x] == 1:
                    self.start_aliens.append([x * 30, y * 30])
                    # print(len(Alien.aliens))

            return new_map

    def affichage_map(self, active_map):
        # print(active_map)
        fen.blit(textures[0], (0, 0))
        for y in range(len(active_map)):
            for x in range(len(active_map[y])):
                # print(active_map[y][x])
                if active_map[y][x] != 0:
                    # print("test")
                    fen.blit(textures[active_map[y][x]], (30 * x, 30 * y))

    def level_up(self, a):
        continuer = True
        while continuer:
            fen.blit(intro, (0, 0))
            if a < len(intros):
                fen.blit(intros[a], (130, 0))
            for event in py.event.get():
                if event.type == py.KEYDOWN:
                    continuer = False
            py.display.flip()
        global Level, active_map
        self.active_map = self.n_map(self.levels[a])


#####################################################fonctions#####################################################
def move_bullets():
    for x in range(len(bullets)):
        if bullets[x][2] == 0:
            bullets[x][0] -= 5
            fen.blit(py.transform.flip(bullet, True, False), (bullets[x][0], bullets[x][1]))
        else:
            bullets[x][0] += 5
            fen.blit(bullet, (bullets[x][0], bullets[x][1]))

def collision():
    a=0
    while a < len(bullets):
    #for a in range(len(bullets)):
        if bullets[a][3] == "player":
            b=0
            while b < len(Alien.aliens):
            #for b in range(len(Alien.aliens)):
                if bullets[a][0]+2 >= Alien.aliens[b].x and bullets[a][0]+2 <= Alien.aliens[b].x + 30 and bullets[a][1] >= Alien.aliens[b].y and bullets[a][1] <= Alien.aliens[b].y + 30:
                    #print("touché")
                    bullets.pop(a)
                    Alien.aliens.pop(b)
                    break
                b+= 1

        else:
            if bullets[a][0] + 2 >= player.x and bullets[a][0] + 2 <= player.x + 30 and bullets[a][1] >= player.y and bullets[a][1] <= player.y + 30:
                bullets.pop(a)
                global game
                game = False
        try:
            if L.active_map[int(bullets[a][1]/30)][int(bullets[a][0]/30)] == 1:
                bullets.pop(a)
        except:
            pass

        a += 1

    if player.finish_coo[0]<= player.x+ 15 and player.finish_coo[0] + 15>= player.x and player.finish_coo[1]<= player.y+ 15 and player.finish_coo[1] + 15>= player.y and len(Alien.aliens) == 0:
        game = False
        #print("test")

            
#####################################################chargement images#####################################################
py.init()
fen = py.display.set_mode((1200, 600))

intro = py.image.load("images/intros/intro.png")
intros = [py.image.load("images/intros/texte_intro_01.png"),
          py.image.load("images/intros/texte_intro_02.png")
          ]

background = py.image.load("images/map/fond2.png")
background.convert()
wall = py.image.load("images/map/roche.png")
wall.convert()
ladder = py.image.load("images/map/echelle.png")
ladder.convert()
door = py.image.load("images/map/door.png")
door.convert()

textures = [background, wall, ladder, door]

player_0 = py.image.load("images/player_0.png")
player_1 = py.image.load("images/player_1.png")
player_2 = py.image.load("images/player_2.png")

right_walk = [player_0, player_1, player_0, player_2]
left_walk = [py.transform.flip(x, True, False) for x in right_walk] #méthode trouvée sur https://fr.acervolima.com/pygame-retournez-l-image/#:~:text=Pour%20retourner%20l%27image%2C%20nous,ou%20horizontal%20selon%20nos%20besoins.

skin_alien = [[py.image.load("images/aliens/alien_0.png"),
               py.image.load("images/aliens/alien_1.png"),
               py.image.load("images/aliens/alien_2.png")]]
skin_alien.append([py.transform.flip(x, True, False) for x in skin_alien[0]])

bullet = py.image.load("images/bullet.png")

bomb = py.image.load("images/bomb.png")

#####################################################sound#####################################################
boom = py.mixer.Sound("sound/boom.wav")
gun = py.mixer.Sound("sound/gun.wav")
timer = py.mixer.Sound("sound/timer.wav")
#####################################################variables#####################################################



player = Joueur(30, 30)

bullets = []

clock = py.time.Clock()



def main(map):
    bullets = []
    global game
    game = True
    while game:
        L.affichage_map(L.active_map)
        player.move()
        
        Alien.fire()
        Alien.show()
        
        move_bullets()

        collision()

        font = py.font.SysFont(None, 24)
        mun = font.render(str(player.munition), True, (0, 0, 0))
        fen.blit(mun, (10, 10))
        bom = font.render(str(player.bomb_reload), True, (0, 0, 0))
        fen.blit(bom, (10, 30))

        
        #print(player.y, player.chute)
        clock.tick(30)
        py.display.flip()

L = Level()
L.level_up(Level.level)
while L.level < len(L.levels):
    Alien.aliens = []

    bullets = []
    player.bomb = []
    player.bomb_reload = 1

    player.x = player.spawn_coo[0]
    player.y = player.spawn_coo[1]

    for x in range(len(L.start_aliens)):
        Alien.aliens.append(Alien(L.start_aliens[x][0], L.start_aliens[x][1]))
    main(L.active_map)
    if player.finish_coo[0] <= player.x + 15 and player.finish_coo[0] + 15 >= player.x and player.finish_coo[1] <= player.y + 15 and player.finish_coo[1] + 15 >= player.y and len(Alien.aliens) == 0:
        L.level += 1
        if L.level <len(L.levels):
            L.level_up(L.level)
        else:
            break
#print(player.spawn_coo)

quit()
