import sys
import pygame as py


link = str(input("file name:\n"))
result = ""
while not(result == "yes" or result == "no"):
    result = str(input("does the file already exist?\n"))


if result == "yes":
    with open(link) as file:
        map = file.read()
        map = map.split("\n")
        map.pop()
        for k in range(0, len(map)):
            map[k] = map[k].split(",")
            for i in range(len(map[k])):
                map[k][i] = int(map[k][i])

else:
    map = [[0 for x in range(40)] for y in range(20)]

if len(map) == 20:
    for y in range(20):
        if len(map[y]) == 40:
            for x in range(40):
                map[y][x] = int(map[y][x])
        else:
            print("y=",y," wrong size")
            sys.exit()
else:
    print("y wrong size")
    sys.exit()
print(map)


class Button:
    """
    inspired by on https://pythonprogramming.altervista.org/buttons-in-pygame/
    Create a button, then blit the surface in the while loop
    """

    def __init__(self, text, pos, img, bg="black"):
        self.x, self.y = pos
        self.font = py.font.SysFont("Arial", 10)
        self.img = img
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        self.text = self.font.render(text, 1, py.Color("White"))
        self.size = self.text.get_size()
        self.surface = py.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = py.Rect(self.x, self.y, self.size[0], self.size[1])


    def show(self):
        fen.blit(self.img, (self.x, self.y))

    def click(self, event):
        x, y = py.mouse.get_pos()
        if event.type == py.MOUSEBUTTONDOWN:
            if py.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    print("click")

def affichage_map(map):
    # print(active_map)
    fen.blit(textures[0], (0, 0))
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] != 0:
                fen.blit(textures[map[y][x]], (30 * x, 30 * y))



py.init()
fen = py.display.set_mode((1400, 600))

background = py.image.load("../images/fond2.png")
background.convert()
wall = py.image.load("../images/roche.png")
wall.convert()
ladder = py.image.load("../images/echelle.png")
ladder.convert()

spawn = py.image.load("../images/player_0.png")
spawn.convert()
alien = py.image.load("../images/alien_0.png")
alien.convert()
finish = py.image.load("../images/door.png")
finish.convert()

textures = [background, wall, ladder, None, None, None, None, None, None, None, alien, spawn, finish]

buttons = []
buttons.append(Button("wall", pos=[1200, 30], img=wall))


continuer = True

while continuer:
    affichage_map(map)

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
        for a in buttons:
            a.click(event)
    for a in buttons:
        a.show()

    py.display.flip()


tk.mainloop()

print(map)



"""
file = open(link, "a")
for i in range(longL):
    for j in range(largL):
        if j == largL-1:
            separateur = "\n"
        else:
            separateur=","
        print(tab[i][j], end=separateur) # print pour comprendre ce qui se passe
        fichier.write(str(tab[i][j])) # ecriture dans le fichier
        fichier.write(separateur)
"""