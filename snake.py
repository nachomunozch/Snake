import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

class Cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dirx = 1, diry = 0, color = red):
        self.pos = start
        self.dirx = dirx
        self.diry = diry
        self.color = color

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, surface, eyes = False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+2, j*dis+2, dis-3, dis-3),0)

        if eyes:
            centre = dis//2
            radius = 3
            center1 = (i*dis+centre-radius, j*dis+8)
            center2 = (i*dis+centre+radius, j*dis+8)
            pygame.draw.circle(surface, black, center1, radius)
            pygame.draw.circle(surface, black, center2, radius)
            
class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirx = 1
        self.diry = 0
        self.lastdir = (self.dirx,self.diry)

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_a]:
                    if not self.lastdir == (1,0):
                        self.dirx = -1
                        self.diry = 0
                        self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                        self.lastdir = (self.dirx,self.diry)

                elif keys[pygame.K_d]:
                    if not self.lastdir == (-1,0):
                        self.dirx = 1
                        self.diry = 0
                        self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                        self.lastdir = (self.dirx,self.diry)

                elif keys[pygame.K_w]:
                    if not self.lastdir == (0,1):
                        self.dirx = 0
                        self.diry = -1
                        self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                        self.lastdir = (self.dirx,self.diry)

                elif keys[pygame.K_s]:
                    if not self.lastdir == (0,-1):
                        self.dirx = 0
                        self.diry = 1
                        self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                        self.lastdir = (self.dirx,self.diry)

        for i, c in enumerate(self.body):       
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.diry == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.diry == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                else: c.move(c.dirx,c.diry)

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface,True)
            else:
                c.draw(surface)
                
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1,tail.pos[1]),dirx=dx,diry=dy))
        if dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1,tail.pos[1]),dirx=dx,diry=dy))
        if dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]-1),dirx=dx,diry=dy))
        if dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]+1),dirx=dx,diry=dy))
        

    def reset(self,pos):
        
        self.body = []
        self.turns = {}
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirx = 1
        self.diry = 0
        self.lastdir = (self.dirx,self.diry)    
    
def draw_grid(w, r, s):
    sizeBtw = w // r
    x = 0
    y = 0
    for l in range(r+1):
        pygame.draw.line(s, black, (x,0), (x,w))
        pygame.draw.line(s, black, (0,y), (w,y))
        x = x + sizeBtw
        y = y + sizeBtw

def redraw_window(surface):
    global width, rows, s, snack
    
    surface.fill(white)
    draw_grid(width, rows, surface)
    s.draw(surface)
    snack.draw(surface)
    
    pygame.display.update()

def random_snack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x,y)

def message_box(subject,content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    
    win = pygame.display.set_mode((width, width))
    s = Snake(red, (10,10))
    snack = Cube(random_snack(rows, s), color = green)

    clock = pygame.time.Clock()

    flag = True
    
    # MAIN LOOP
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(random_snack(rows, s), color = green)

        for x in s.body[1:]:
            if s.body[0].pos == x.pos:
                message_box("You Lost","Play again...")
                s.reset((10,10))
                break
        
        redraw_window(win)

main()
