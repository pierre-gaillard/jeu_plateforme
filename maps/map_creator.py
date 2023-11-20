import sys
import pygame as py

link = str(input("file name:\n"))
result = ""
while not(result == "yes" or result == "no"):
    result = str(input("does the file already exist?\n"))


if result == "yes":
    with open(link) as file:
        amap = file.read()
        amap = amap.split("\n")
        amap.pop()
        for k in range(0, len(amap)):
            amap[k] = amap[k].split(",")
            for i in range(len(amap[k])):
                amap[k][i] = int(amap[k][i])

else:
    amap = [[0 for x in range(40)] for y in range(20)]

print(amap)
if len(amap) == 20:
    for y in range(20):
        if len(amap[y]) == 40:
            for x in range(40):
                amap[y][x] = int(amap[y][x])
        else:
            print("y=", y, " wrong size")
            sys.exit()
else:
    print(f"y={y} wrong size")
    sys.exit()
print(amap)

py.init()
fen = py.display.set_mode((1230, 600))
fen.fill([255, 255, 255])


class Button:
    """
    inspired by on https://pythonprogramming.altervista.org/buttons-in-pygame/
    Create a button, then blit the surface in the while loop
    """

    def __init__(self, text, pos, img, bg="white"):
        self.x, self.y = pos
        self.font = py.font.SysFont("Arial", 10)
        self.img = img
        self.change_text(text, bg)

    def change_text(self, text, bg):
        self.text = self.font.render(text, 1, py.Color("black"))
        #self.size = self.img.get_size()
        self.surface = py.Surface([30,40])
        self.surface.blit(self.text, (0, 0))
        self.rect = py.Rect(self.x, self.y, 30, 40)

    def show(self):
        if self.img != None:
            fen.blit(self.img, (self.x, self.y+10))
        fen.blit(self.text, (self.x, self.y))

    def click(self, event):
        x, y = py.mouse.get_pos()
        if event.type == py.MOUSEBUTTONDOWN:
            if py.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False


class Map:
    def __init__(self):
        self.map = amap

    def show_map(self):
        """shows the map"""
        fen.blit(textures[0], (0, 0))
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] != 0:
                    fen.blit(textures[self.map[y][x]], (30 * x, 30 * y))


background = py.image.load("../images/map/fond2.png")
background.convert()
wall = py.image.load("../images/map/roche.png")
wall.convert()
ladder = py.image.load("../images/map/echelle.png")
ladder.convert()

spawn = py.image.load("../images/player/player_0.png")
spawn.convert()
alien = py.image.load("../images/aliens/alien_0.png")
alien.convert()
finish = py.image.load("../images/map/door.png")
finish.convert()

actual_map = Map()
textures = [background, wall, ladder, None, None, None, None, None, None, None, alien, spawn, finish]
names = ["background", "wall", "ladder", None, None, None, None, None, None, None, "alien", "spawn", "finish"]

buttons = [Button(names[0], pos=[1200, 0], img=None)]
length = 1
for i in range(1, len(textures)):
    if textures[i] != None:
        buttons.append(Button(names[i], pos=[1200, 40*length], img=textures[i]))
        length += 1
    else:
        buttons.append(None)

selected = 1

continuer = True

while continuer:
    actual_map.show_map()
    py.display.flip()

    for a in buttons:
        if a != None:
            a.show()
    for event in py.event.get():
        if py.mouse.get_pressed()[0]:
            x, y = py.mouse.get_pos()
            if x < 1200:
                actual_map.map[int(y/30)][int(x/30)] = selected
        for a in buttons:
            if a != None:
                if a.click(event):
                    selected = buttons.index(a)
        if event.type == py.QUIT:
            py.quit()
            continuer = False


#print(actual_map.active_map)

"""méthode pour creer un fichier csv donnee par M Garin"""

file = open(link, "a")
print(len(actual_map.map), len(actual_map.map[0]))
for i in range(len(actual_map.map)):
    for j in range(len(actual_map.map[i])):
        if j == len(actual_map.map[i])-1:
            separateur = "\n"
        else:
            separateur=","
        print(actual_map.map[i][j], end=separateur) # print pour comprendre ce qui se passe
        file.write(str(actual_map.map[i][j])) # ecriture dans le fichier
        file.write(separateur)
file.close() # en fermant le fichier, il s'enregistre dans le rep local.
