import pygame as py


class Button:
    """
    Create a button, then blit the surface in the while loop
    """

    def __init__(self, anchor, pos=[0, 0], size=[0, 0], bg=None, text="", font=["arial", 10], color="black",
                 img=None):
        """
        :param anchor: the window where the button is
        :param pos: position of the button
        :param size: (optional if there is an image)
        :param bg: background of the button
        :param text: (optional) text on the button
        :param font: (optional) font of the text
        :param color: (optional) color of the text
        :param img: (optional) image on the button
        """
        self.anchor = anchor
        self.x, self.y = pos
        self.bg = bg
        self.font = py.font.SysFont(font[0], font[1])
        self.color = color
        self.text = text
        self.label = self.font.render(self.text, 1, self.color)
        self.img = img
        if self.img != None and size == [0, 0]:
            self.size = self.img.get_size()
        else:
            self.size = size
        self.rect = py.Rect(self.x, self.y, self.size[0], self.size[1])

    def __str__(self):
        return str({"anchor": self.anchor, "pos": [self.x, self.y], "bg": self.bg, "font": self.font,
                    "color": self.color, "text": self.text, "img": self.img, "size": self.size, "rect": self.rect})

    def change(self, pos: object = None, size: object = None, bg: object = None, text: object = None, font: object = None, color: object = None, img: object = None) -> object:
        """
        chose wich parameter you want to change
        """
        if pos != None:
            self.x, self.y = pos
        if size != None:
            self.size = size
        if bg != None:
            self.bg = bg
        if text != None:
            self.text = text
        if font != None:
            self.font = py.font.SysFont(font[0], font[1])
        if color != None:
            self.color = color
        if img != None:
            self.img = img
        self.label = self.font.render(self.text, 1, py.Color(self.color))
        self.rect = py.Rect(self.x, self.y, self.size[0], self.size[1])
        return None

    def show(self):
        """
        shows the button, the image and text
        """
        if self.bg != None:
            py.draw.rect(self.anchor, self.bg, py.Rect(self.x, self.y, self.size[0], self.size[1]))
        if self.img != None:
            self.anchor.blit(self.img, (self.x, self.y))
        self.anchor.blit(self.label, (self.x, self.y))

    def click(self, event):
        x, y = py.mouse.get_pos()
        if event.type == py.MOUSEBUTTONDOWN and py.mouse.get_pressed()[0]:
            if self.rect.collidepoint(x, y):
                    return True
        return False


class Scrollbar:
    """
    shows a scrollbar
    """
    class Scroll:
        def __init__(self, anchor, pos, size, max_movement, bg="light gray", color="dark gray"):
            self.anchor = anchor
            self.x, self.y = pos
            self.size = size
            self.bg = bg
            self.color = color
            self.is_pressed = False
            self.max_movement = max_movement

        def show(self):
            py.draw.rect(self.anchor, self.bg,
                         py.Rect(self.x, self.max_movement[0], self.size[0], self.max_movement[1]))
            py.draw.rect(self.anchor, self.color, py.Rect(self.x+1, self.y, self.size[0]-2, self.size[1]))

        def move(self):
            x, y = py.mouse.get_pos()
            rect = py.Rect(self.x, self.max_movement[0], self.size[0], self.max_movement[1])
            if py.mouse.get_pressed()[0] and rect.collidepoint(x, y):
                self.is_pressed = True
            if not(py.mouse.get_pressed()[0]):
                self.is_pressed = False

            if self.is_pressed:
                self.y = y-(self.size[1]/2)
            if self.y < self.max_movement[0]+1:
                self.y = self.max_movement[0]+1
            elif self.y+self.size[1] > self.max_movement[1]-1:
                self.y = self.max_movement[1]-self.size[1]-1

    def __init__(self, anchor, pos=(0, 0), size=[100, 100], bg=None, item_height=10, items=[], scroll_width=10):
        self.anchor = anchor
        self.x, self.y = pos
        self.size = size
        self.rect = py.Rect(self.x, self.y, self.size[0], self.size[1])
        self.bg = bg
        self.item_height = item_height
        self.shown = [self.y, self.y+self.size[1]]
        self.items = [Button(anchor, pos=(self.x, self.y+i*self.item_height), size=[self.size[0]-2, self.item_height], text=items[i])
                      for i in range(len(items))]

        if len(items) > (len(items)*item_height)/size[1]:
            scroll_height = (size[1]-2) * (size[1]/(len(items)*item_height))
            #print("true", (size[1]/((len(items)+1)*item_height)))
        else:
            scroll_height = size[1]-2
            #print("false")
        self.scroll = self.Scroll(anchor=self.anchor, pos=[self.x+self.size[0]-2, self.y],
                                  size=[scroll_width, scroll_height], max_movement=[self.y, self.y+self.size[1]])

    def update(self):
        scroll_diff = (self.scroll.y - self.y) / (self.size[1] - self.scroll.size[1] - 1)
        self.shown = [scroll_diff, scroll_diff + self.size[1]]
        for i in range(len(self.items)):
            self.items[i].change(pos=[self.items[i].x,
                                  i * self.item_height - scroll_diff * len(self.items) * self.item_height + 10])

    def show(self):
        if self.bg != None:
            py.draw.rect(self.anchor, self.bg, self.rect)
        for i in range(len(self.items)):
            if self.y-1 <= self.items[i].y <= self.y+self.size[1]-self.item_height+1:
                self.items[i].show()
        self.update()
        self.scroll.show()
        self.scroll.move()

    def item_pressed(self, event):
        return [item.click(event) for item in self.items]



