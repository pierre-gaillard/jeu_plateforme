import pygame as py
import random, time
from math import *


#####################################################joueur#####################################################


class Joueur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spawn_coo = []
        self.finish_coo = []
        self.skin = 0

        self.munition = 2  # 2 est le max
        self.reload = 0.01
        self.chute = 0

        self.direction = 1  # 0 = left , 1 = right
        self.animation = 0  # pour le déplacement

        self.bomb = []  # x, y, deltax, deltay
        self.bomb_reload = 1
        self.bomb_timer = 100

        self.life = 3

    def move(self):
        '''
        allows the player to move and quit
        allows to reload the gun and the bomb
        '''
        global game, level

        """gravity"""
        if L.active_map[int((self.y + 30) / 30)][int((self.x + 7) / 30)] == 1 or L.active_map[int((self.y + 30) / 30)][
            int((self.x + 23) / 30)] == 1:
            # print("touche")
            self.chute = 0
            self.y = 10 * int(self.y / 10)  # pour que ca s'arrete pile sur le sol

        else:
            self.chute += 0.14

        if L.active_map[int((self.y + 30) / 30)][int((self.x + 20) / 30)] == 2:
            self.chute = 0

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                """fire"""
                if event.key == py.K_SPACE and self.munition >= 1:
                    bullets.append(
                        [self.x + 30 if self.direction == 1 else self.x - 6, self.y + 10, self.direction, "player"])
                    self.munition -= 1
                    gun.play()
                """drop a bomb"""
                if event.key == py.K_c and self.bomb_reload >= 1 and L.level > 0:
                    self.bomb = [self.x, self.y, -2 if self.direction == 0 else 2, 0]
                    self.bomb_reload = 0
                    self.bomb_timer = 300
                    timer.play()
                    # py.mixer.Sound.set_volume(100)
                """restart the level"""
                if event.key == py.K_r:
                    game = False

                """change skin"""
                if event.key == py.K_n:
                    self.skin += 1
                    if self.skin == len(right_walk):
                        self.skin = 0
                """quit the game"""
                if event.key == py.K_ESCAPE:
                    game = False
                    L.level = 1000
        keys = py.key.get_pressed()
        # move
        """jump, climb stair or fly"""
        if (keys[py.K_z] or keys[py.K_UP]):
            # print(L.level)
            if L.active_map[int((self.y + 30) / 30)][int((self.x + 7) / 30)] == 1 or \
                    L.active_map[int((self.y + 30) / 30)][int((self.x + 23) / 30)] == 1:
                self.chute = -3
            elif L.active_map[int((self.y + 30) / 30)][int((self.x + 15) / 30)] == 2 and not (
                    L.active_map[int((self.y) / 30)][int((self.x + 7) / 30)] == 1 or L.active_map[int((self.y) / 30)][
                int((self.x + 23) / 30)] == 1):
                self.chute = -3
            # fly
            elif (L.level == len(L.levels) - 1 and not (
                    L.active_map[int((self.y) / 30)][int((self.x + 7) / 30)] == 1 or L.active_map[int((self.y) / 30)][
                int((self.x + 23) / 30)] == 1)) and self.chute > -7:
                self.chute -= 0.7
                fen.blit(prop[self.direction], (self.x, self.y))
        """go down ladders"""
        if (keys[py.K_s] or keys[py.K_DOWN]) and L.active_map[int((self.y + 30) / 30)][int((self.x + 15) / 30)] == 2:
            self.chute = 3
        """walk left"""
        if (keys[py.K_q] or keys[py.K_LEFT]) and (
                L.active_map[int((self.y) / 30)][int((self.x + 5) / 30)] != 1 and L.active_map[int((self.y + 27) / 30)][
            int((self.x + 5) / 30)] != 1):
            self.x -= 3
            self.direction = 0
        """walk right"""
        if (keys[py.K_d] or keys[py.K_RIGHT]) and (L.active_map[int((self.y) / 30)][int((self.x + 25) / 30)] != 1 and
                                                   L.active_map[int((self.y + 29) / 30)][int((self.x + 25) / 30)] != 1):
            self.x += 3
            self.direction = 1

        """collisions"""
        if L.active_map[int((self.y) / 30)][int((self.x + 15) / 30)] == 1:
            self.chute = 0.6

        if not (keys[py.K_q] or keys[py.K_LEFT] or keys[py.K_d] or keys[py.K_RIGHT]):
            self.animation = 0
        else:
            self.animation += 0.1

        if self.animation >= 4:
            self.animation = 0

        self.y += self.chute

        self.show()

        """fire reload"""
        if self.munition <= 2:
            if self.reload >= 1:
                self.munition += 1
                self.reload = 0
            self.reload += 0.02

    def move_bomb(self):
        """
        move the player's bomb
        makes the bomb explode
        """
        # bomb move
        if self.bomb != []:
            try:  # la bombe peut aller trop bas à cause de la vitesse et passer sous la map
                if L.active_map[int((self.bomb[1] + 5) / 30)][int((self.bomb[0] + 2.5) / 30)] == 1:
                    while L.active_map[int((self.bomb[1]) / 30)][int((self.bomb[0] + 2.5) / 30)] == 1 and self.bomb[
                        3] > 0:
                        self.bomb[1] -= 30
                    self.bomb[3] = -0.75 * self.bomb[3]
                    self.bomb[1] = (int(self.bomb[1] / 30)) * 30 + 25

                # print("tried")
            except:
                self.bomb[3] = -0.75 * self.bomb[3]
                self.bomb[1] = 565
            if L.active_map[int((self.bomb[1]) / 30)][int((self.bomb[0] + 2.5) / 30)] == 1:
                self.bomb[3] = -0.75 * self.bomb[3]
                self.bomb[1] = (int(self.bomb[1] / 30)) * 30 + 35
            try:  # la bombe peut aller trop bas à cause de la vitesse et passer sous la map
                if L.active_map[int((self.bomb[1] + 2.5) / 30)][int((self.bomb[0]) / 30)] == 1:
                    self.bomb[2] = -0.75 * self.bomb[2]
                    self.bomb[0] = (int(self.bomb[0] / 30)) * 30 + 30
            except:
                self.bomb[3] = -0.75 * self.bomb[3]
                self.bomb[1] = 565
            if L.active_map[int((self.bomb[1] + 2.5) / 30)][int((self.bomb[0] + 5) / 30)] == 1:
                self.bomb[2] = -0.75 * self.bomb[2]
                self.bomb[0] = (int(self.bomb[0] / 30)) * 30 + 15

            self.bomb[0] += self.bomb[2]
            self.bomb[1] += self.bomb[3]
            self.bomb[2] = 0.99 * self.bomb[2]
            self.bomb[3] += 0.28
            fen.blit(bomb, (self.bomb[0], self.bomb[1]))
            self.bomb_timer -= 2

            # explode
            if self.bomb_timer <= 0:
                new_aliens = []
                # py.mixer.timer.set_volume(0)
                boom.play()
                for a in Alien.aliens:
                    # print(sqrt((((a.x + 15)-(self.bomb[0]+2.5))**2)+(((a.y+15)-(self.bomb[1]+2.5))**2)))
                    if sqrt((((a.x + 15) - (self.bomb[0] + 2.5)) ** 2) + (
                            ((a.y + 15) - (self.bomb[1] + 2.5)) ** 2)) >= 90:
                        new_aliens.append(a)
                    Alien.aliens = new_aliens
                if sqrt((((self.x + 15) - (self.bomb[0] + 2.5)) ** 2) + (
                        ((self.y + 15) - (self.bomb[1] + 2.5)) ** 2)) <= 90:
                    # global game
                    game = False

                self.bomb = []
        elif self.bomb_reload < 1:
            self.bomb_reload = round(self.bomb_reload + 0.01, 3)
        else:
            self.bomb_reload = 1

    def show(self):
        """show player"""
        if self.direction == 0:
            fen.blit(left_walk[self.skin][int(self.animation)], (self.x, self.y))
        else:
            fen.blit(right_walk[self.skin][int(self.animation)], (self.x, self.y))

        if L.level >= len(L.levels) - 1:
            for i in range(1, 4):
                if self.life >= i:
                    fen.blit(life[1], (1000 + 23 * i, 20))
                else:
                    fen.blit(life[0], (1000 + 23 * i, 20))


#####################################################alien#####################################################
class Alien:
    aliens = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reload = 1
        self.direction = random.randint(0, 1)
        self.skin = random.randint(0, 2)

    def show():
        """shows all the aliens"""
        for mob in Alien.aliens:
            fen.blit(skin_alien[mob.direction][mob.skin], (mob.x, mob.y))

    def fire():
        """
        tries to fire on the player if it is possible
        reload the gun of each alien
        """
        for mob in Alien.aliens:
            mob.reload += 0.01
            fire = True
            direction = 0
            if mob.reload >= 1 and abs(mob.y - player.y) <= 20:
                if mob.x <= player.x:
                    direction = 1
                    for a in range(int(mob.x / 30), int(player.x / 30)):
                        # print(active_map[4][a])
                        if L.active_map[int(mob.y / 30)][a] == 1:
                            fire = False
                else:
                    direction = 0
                    for a in range(int(player.x / 30), int(mob.x / 30)):
                        if L.active_map[int(mob.y / 30)][a] == 1:
                            fire = False

                if fire:
                    a = int(player.x / 30) - 1
                    bullets.append([mob.x + 30 if direction == 1 else mob.x - 6, mob.y + 10, direction, "alien"])
                    # print("fire")
                    mob.direction = 0 if direction == 1 else 1
                    mob.reload = 0
                    gun.play()


#####################################################Boss alien#####################################################
class BossAlien:
    def __init__(self):
        self.x = 900
        self.y = 220
        self.grav = 0
        self.movement = 0
        self.dir = 0
        self.bullet = []
        self.life = 100

    def show(self):
        """shows the boss and it's life bar"""
        fen.blit(skin_BossAlien[self.dir], (self.x, self.y))
        # fen.blit(bullet, (self.x+150, self.y))
        fen.blit(boss_empty, (self.x + 50, self.y - 30))
        for i in range(self.life):
            fen.blit(boss_bar, (self.x + 2 * (i + 1) + 50, self.y - 28))

    def move(self):
        """makes the boss and its bullets move"""
        """orientation"""
        if self.x + 150 < player.x + 15:
            self.dir = 1
        else:
            self.dir = 0

        """gravity and move"""
        # modify gravity
        if self.y + 301 <= 540:
            self.grav += 0.1
        else:
            self.grav = 0
        # stop the boss from moving
        if -0.01 < self.movement < 0.01:
            self.movement = 0
        else:
            self.movement = 0.98 * self.movement
        # apply gravity
        self.y += self.grav
        # when the boss touches the roof
        if self.y < 30 and self.grav > 0:
            self.grav = -0.75 * self.grav
            self.y += 2
        # modify the movement of the boss
        if 60 < self.x < 960:
            self.x += self.movement
        else:
            self.movement = -0.75 * self.movement
            self.x += self.movement

        """random jump"""
        if random.randint(0, 1000) <= 10 and self.y + 300 >= 400:
            self.grav = -3
            self.y -= 10
            self.movement = random.randint(-20, 20)

        """show the boss"""
        self.show()

        """move the bullets"""
        new_bullet = []
        for i in self.bullet:
            # print(i[4])
            i[0] += i[2]
            i[1] += i[3]
            orient = -50 * i[4]
            if i[5] == 0:
                orient += 180
            fen.blit(py.transform.rotate(boss_bullet, orient), (i[0], i[1]))
            if 60 < i[0] < 1140 and 60 < i[1] < 525:
                new_bullet.append(i)
                # kill the player
                if i[0] + 5 >= player.x and i[0] + 2 <= player.x + 30 and i[1] >= player.y and i[1] <= player.y + 30:
                    player.life -= 1
                    if player.life <= 0:
                        global game
                        game = False
                        self.life = 100
                        player.life = 3
                    new_bullet.pop()
        self.bullet = new_bullet

    def fire(self):
        """fire"""
        if self.dir == 0:
            angle = atan((self.y + 120 - (player.y + 15)) / (self.x + 10 - (player.x + 15)))
            self.bullet.append([self.x + 10, self.y + 110, -7 * cos(angle), -7 * sin(angle), angle, 0])
        else:
            angle = atan((self.y + 120 - (player.y + 15)) / (self.x + 290 - (player.x + 15)))
            self.bullet.append([self.x + 290, self.y + 110, 7 * cos(angle), 7 * sin(angle), angle, 1])

    def star_fire(self):
        """fires in 25 different directions"""
        for i in range(25):
            x = self.x + 150
            y = self.y + 150
            angle = i * (2 * pi) / 24
            direct = 0 if i <= 12 else 1
            self.bullet.append([x, y, 7 * cos(angle), 7 * sin(angle), angle, direct])

    def random_fire(self):
        """normal fire"""
        if random.randint(0, 100) <= 2 and abs(self.x + 150 - player.x + 15) > 150:
            self.fire()

        """star fire"""
        if random.randint(0, 1000) <= 2 and abs(self.x + 150 - player.x + 15) > 100:
            self.star_fire()

    def lose_life(self):
        """removes life to the boss if it touches a player's bullet"""
        global bullets
        new_bullet = []
        for i in bullets:
            if self.x + 100 < i[0] < self.x + 185 and self.y + 16 < i[1] < self.y + 285:
                self.life -= 5
                boss_damage.play()
            else:
                new_bullet.append(i)
        bullets = new_bullet

        if self.life <= 0:
            win()


#####################################################level#####################################################
class Level:
    level = 0
    levels = [["maps/map_01.csv", 0], ["maps/map_02.csv", 15], ["maps/map_03.csv", 20], ["maps/map_04.csv", 30],
              ["maps/map_boss.csv", 0]]
    intro = py.image.load("images/intros/intro.png")
    intros = [py.image.load("images/intros/texte_intro_01.png"),
              py.image.load("images/intros/texte_intro_02.png"),
              py.image.load("images/intros/texte_intro_03.png"),
              None,
              py.image.load("images/intros/texte_intro_boss.png")
              ]

    def __int__(self):
        active_map = n_map(levels[Level.level])
        start_aliens = []

    def n_map(self, lien):
        """
        changes the actual map
        input:
            -link of the new map (str ex: 'maps/test.csv')
        return:
            -the new map(list of list [[],[]...])
        """
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

    def show_map(self, active_map):
        """shows the map"""
        # print(active_map)
        fen.blit(textures[0], (0, 0))
        for y in range(len(active_map)):
            for x in range(len(active_map[y])):
                # print(active_map[y][x])
                if active_map[y][x] != 0:
                    # print("test")
                    fen.blit(textures[active_map[y][x]], (30 * x, 30 * y))

    def level_up(self, a):
        """
        shows the help for the new level
        changes the actual map
        input:
            -level (int)
        """
        continuer = True
        # py.mixer.music.fadeout(60)
        py.mixer.music.stop()
        while continuer:
            fen.blit(L.intro, (0, 0))
            if a < len(L.intros) and L.intros[a] != None:
                fen.blit(L.intros[a], (130, 0))
            for event in py.event.get():
                if event.type == py.KEYDOWN:
                    continuer = False
            py.display.flip()
        global Level, active_map
        py.mixer.music.play(-1, 0.0, 5)
        self.active_map = self.n_map(self.levels[a])


#####################################################fonctions#####################################################
def move_bullets():
    """moves all the bullets(player and alien)"""
    for x in range(len(bullets)):
        if bullets[x][2] == 0:
            bullets[x][0] -= 5
            fen.blit(py.transform.flip(bullet, True, False), (bullets[x][0], bullets[x][1]))
        else:
            bullets[x][0] += 5
            fen.blit(bullet, (bullets[x][0], bullets[x][1]))


def collision():
    """
    looks if the player or an alien is killed
    looks if the player has finished the level
    """
    a = 0
    while a < len(bullets):
        # for a in range(len(bullets)):
        if bullets[a][3] == "player":
            b = 0
            while b < len(Alien.aliens):
                # for b in range(len(Alien.aliens)):
                if bullets[a][0] + 2 >= Alien.aliens[b].x and bullets[a][0] + 2 <= Alien.aliens[b].x + 30 and \
                        bullets[a][1] >= Alien.aliens[b].y and bullets[a][1] <= Alien.aliens[b].y + 30:
                    # print("touché")
                    bullets.pop(a)
                    Alien.aliens.pop(b)
                    break
                b += 1

        else:
            if bullets[a][0] + 2 >= player.x and bullets[a][0] + 2 <= player.x + 30 and bullets[a][1] >= player.y and \
                    bullets[a][1] <= player.y + 30:
                bullets.pop(a)
                global game
                game = False
        try:
            if L.active_map[int(bullets[a][1] / 30)][int(bullets[a][0] / 30)] == 1:
                bullets.pop(a)
        except:
            pass

        a += 1

    if player.finish_coo[0] <= player.x + 15 and player.finish_coo[0] + 15 >= player.x and player.finish_coo[
        1] <= player.y + 15 and player.finish_coo[1] + 15 >= player.y and len(Alien.aliens) == 0 and L.level != len(
        L.levels) - 1:
        game = False
        # print("test")


def win():
    """
    win animation
    shows the time of the player
    """
    global game, timer_start
    game = False
    L.level = 1000
    font1 = py.font.SysFont(None, 50)
    win_text = font1.render("YOU WIN !", True, (255, 255, 255))

    font2 = py.font.SysFont(None, 40)
    score1 = font2.render("YOU FINISHED IN:", True, (255, 255, 255))

    timer = int(time.time() - timer_start)
    min = timer // 60
    timer = timer % 60
    hour = min // 60
    min = min % 60
    score2 = font2.render(f"{hour} : {min} : {timer}", True, (255, 255, 255))

    continuer = True
    py.mixer.music.stop()
    spaceship.play()
    while continuer:
        fen.blit(end, (0, 0))
        fen.blit(win_text, (500, 280))
        fen.blit(score1, (480, 320))
        fen.blit(score2, (520, 350))
        py.display.flip()
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    continuer = False


#####################################################chargement images#####################################################
py.init()
fen = py.display.set_mode((1200, 600))

background = py.image.load("images/map/fond3.png")
background.convert()
wall = py.image.load("images/map/roche.png")
wall.convert()
ladder = py.image.load("images/map/echelle.png")
ladder.convert()
door = py.image.load("images/map/door.png")
door.convert()

textures = [background, wall, ladder, door]

player_0 = py.image.load("images/player/player_0.png")
player_1 = py.image.load("images/player/player_1.png")
player_2 = py.image.load("images/player/player_2.png")

right_walk = [[player_0, player_1, player_0, player_2]]
left_walk = [[py.transform.flip(x, True, False) for x in right_walk[
    0]]]  # méthode trouvée sur https://fr.acervolima.com/pygame-retournez-l-image/#:~:text=Pour%20retourner%20l%27image%2C%20nous,ou%20horizontal%20selon%20nos%20besoins.

player_0_blue = py.image.load("images/player/player_0_blue.png")
player_1_blue = py.image.load("images/player/player_1_blue.png")
player_2_blue = py.image.load("images/player/player_2_blue.png")

right_walk.append([player_0_blue, player_1_blue, player_0_blue, player_2_blue])
left_walk.append([py.transform.flip(x, True, False) for x in right_walk[1]])

life = (py.image.load("images/life/empty.png"), py.image.load("images/life/full.png"))

prop = [py.transform.flip(py.image.load("images/player/prop.png"), True, False),
        py.image.load("images/player/prop.png")]

skin_alien = [[py.image.load("images/aliens/alien_0.png"),
               py.image.load("images/aliens/alien_1.png"),
               py.image.load("images/aliens/alien_2.png")]]
skin_alien.append([py.transform.flip(x, True, False) for x in skin_alien[0]])

skin_BossAlien = [0, py.image.load("images/boss.png")]
skin_BossAlien[0] = py.transform.flip(skin_BossAlien[1], True, False)

boss_empty = py.image.load("images/life/boss_empty.png")
boss_bar = py.image.load("images/life/boss_bar.png")

bullet = py.image.load("images/bullet.png")
boss_bullet = py.image.load("images/boss_bullet.png")

bomb = py.image.load("images/bomb.png")

end = py.image.load("images/end.png")

#####################################################sound#####################################################
music = py.mixer.music.load("sound/main_2.wav")
boom = py.mixer.Sound("sound/boom.wav")
gun = py.mixer.Sound("sound/gun.wav")
timer = py.mixer.Sound("sound/timer.wav")
boss_damage = py.mixer.Sound("sound/boss_damage.wav")
spaceship = py.mixer.Sound("sound/spaceship.wav")
#####################################################variables#####################################################

player = Joueur(30, 30)

bullets = []

clock = py.time.Clock()

timer_start = time.time()


def main(map):
    """
    main program of the game
    input:
        -map (list)
    """
    bullets = []
    global game
    game = True
    if L.level == len(L.levels) - 1:
        boss = BossAlien()
    while game:
        L.show_map(map)
        player.move()
        player.move_bomb()

        Alien.fire()
        Alien.show()
        if L.level == len(L.levels) - 1:
            boss.random_fire()
            boss.move()
            boss.lose_life()

        move_bullets()

        collision()

        font = py.font.SysFont(None, 24)
        mun = font.render(str(player.munition), True, (0, 0, 0))
        fen.blit(mun, (10, 10))
        bom = font.render(str(player.bomb_reload), True, (0, 0, 0))
        fen.blit(bom, (10, 30))

        # print(player.y, player.chute)
        clock.tick(30)
        py.display.flip()


L = Level()
L.level_up(Level.level)
while L.level < len(L.levels):
    # Alien.aliens = []

    bullets = []
    player.bomb = []
    player.bomb_reload = 1

    player.x = player.spawn_coo[0]
    player.y = player.spawn_coo[1]

    Alien.aliens=[]
    for x in range(len(L.start_aliens)):
        Alien.aliens.append(Alien(L.start_aliens[x][0], L.start_aliens[x][1]))
    main(L.active_map)
    if player.finish_coo[0] <= player.x + 15 and player.finish_coo[0] + 15 >= player.x and player.finish_coo[
        1] <= player.y + 15 and player.finish_coo[1] + 15 >= player.y and len(Alien.aliens) == 0:
        L.level += 1
        if L.level < len(L.levels):
            L.level_up(L.level)
        else:
            break

quit()
