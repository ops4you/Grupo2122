from turtle import pos
import pygame
import argparse
import socket
import threading
import random
import constants
import chars
import os

map1 ="""                             
                             
wwwwwwwwwwwwwwwwwwwwwwwwwwwww
w               w           w
w                           w
w    wwwwww    wwwww      www
www    w                  w w
w      w          w         w
w   wwwww     wwwwwww      ww
w      wwwwww     w     w   w
w    w      w   www  wwww   w
w      w          w     w   w
w   wwwwww www-wwww     w   w
w     w              ww w   w
w                           w
wwwwwwwwwwwwwwwwwwwwwwwwwwwww"""

serverAddressPort   = ("::1",20001)
bufferSize          = 1024

class Game:
    def __init__(self):
        #begin game display
        pygame.init()
        self.display = pygame.display.set_mode((constants.WIDTH,constants.HEIGHT))
        pygame.display.set_caption(constants.GAME_TITLE)
        icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.match_font(constants.FONT)
        self.load_files()
        self.player = ""
        self.p1 = Player(self.bombermanr,4,0,0)
        self.p1.rect.x = 100
        self.p1.rect.y = 100
        self.otherPlayers = []
        self.bombs = [Bomb(0,0),Bomb(0,0),Bomb(0,0),Bomb(0,0)]
        self.i = 0
        self.position = pygame.math.Vector2(0,0) 
        self.pressb = -5000000000
        self.presse = -5000000000
        self.current_time = 0
        self.tile_rects = []
        self.free_map = []
        self.map1 = map1.splitlines()
    

    def new_game(self):
        #inicialize char classes
        self.all_chars = pygame.sprite.Group()
        self.run()

    def run(self):
        #game_loop
        self.playing = True
        while self.playing:
            self.UDPClientSocket = socket.socket(family=socket.AF_INET6, type=socket.SOCK_DGRAM)
            self.clock.tick(60)  
            self.current_time = pygame.time.get_ticks()
            self.events()
            self.update_chars()
            self.draw_chars()

    def events(self):
        #define game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False  
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT:
                    self.p1.x_change = -2
                if event.key == pygame.K_RIGHT:
                    self.p1.x_change = 2
                if event.key == pygame.K_UP:
                    self.p1.y_change = -2
                if event.key == pygame.K_DOWN:
                    self.p1.y_change = 2
                if event.key == pygame.K_SPACE: 
                    if(self.p1.bombs>0 and self.i>=0 and self.i<4):
                         self.pressb = pygame.time.get_ticks()
                         self.bombs[self.i].x = self.p1.rect.x
                         self.bombs[self.i].y = self.p1.rect.y
                         self.p1.bombs -= 1

            if event.type == pygame.KEYUP:
               if event.key == pygame.K_LEFT:
                    self.p1.x_change = 0
               if event.key == pygame.K_RIGHT:
                    self.p1.x_change = 0
               if event.key == pygame.K_UP:
                    self.p1.y_change = 0
               if event.key == pygame.K_DOWN: 
                    self.p1.y_change = 0  
    
    def update_chars(self):
        #update chars
        self.update(self.p1.rect,self.tile_rects,self.p1.x_change,self.p1.y_change)
        msgFromCli1 = str(self.p1.rect.x) + ' ' + str(self.p1.rect.y) + ' '
        msgFromCli2 = ""
        for bomb in self.bombs:
            if bomb.x !=0 and bomb.y != 0:
                msgFromCli2 = msgFromCli2 + str(bomb.x) + ' ' + str(bomb.y) 
        self.msgFromClient = msgFromCli1 + msgFromCli2
        self.bytesToSend = str.encode(self.msgFromClient)
        self.UDPClientSocket.sendto(self.bytesToSend, serverAddressPort)
        pygame.display.update()

    def draw_chars(self):
        #draw chars
        self.display.fill(constants.WHITE) #cleaning display
        
        self.tiles(self.map1)
            
        self.display.blit(self.bomberman,(self.p1.rect.x,self.p1.rect.y))
        self.draw_otherplayers(self.otherPlayers)

        if (self.current_time - self.pressb)<3000:
            self.display.blit(self.bomb,(self.bombs[self.i].x,self.bombs[self.i].y))
        elif((self.current_time - self.pressb)>3000 and self.i>= 0 and self.i<4): 
            pygame.transform.flip(self.bomb,self.bombs[self.i].x,self.bombs[self.i].y)
            self.i =+ 1
  
        pygame.display.flip()

    def load_files(self):
        #load image files
        image_path = os.path.join(os.getcwd(),'images')

        self.bomberman_logo = os.path.join(image_path,constants.LOGO)
        self.bomberman_logo = pygame.image.load(self.bomberman_logo)

        self.bomberman = os.path.join(image_path,constants.BOMBERMAN)
        self.bomberman = pygame.image.load(self.bomberman)
        self.bombermanr = self.bomberman.get_rect()

        self.bomb = os.path.join(image_path,constants.BOMB)
        self.bomb = pygame.image.load(self.bomb)

        #self.explode = os.path.join(image_path,constants.EXPLODE)
        #self.explode = pygame.image.load(self.explode)

        self.wall = os.path.join(image_path,constants.WALL) 
        self.wall = pygame.image.load(self.wall)

        self.wall2 = os.path.join(image_path,constants.WALL2) 
        self.wall2 = pygame.image.load(self.wall2)

    def tiles(self,map1):
     for y, line in enumerate(self.map1):
        for x, c in enumerate(line):
            if c == "w":
                self.display.blit(self.wall2,(x * 30, y * 30))
                self.tile_rects.append(pygame.Rect(x * 30, y * 30, 30, 30))
            else: self.free_map.append(pygame.Rect(x * 30, y * 30, 30, 30))

    def add_otherplayers(self,n):
     for x in range(n):
            self.otherPlayers.append(Player(self.bombermanr,4,0,0))  
     return self.otherPlayers      
    
    def draw_otherplayers(self,otherPlayers):
     for p in otherPlayers:
            self.display.blit(self.bomberman,(200,200))    
                
    def collision_test(self,rect,tiles):
     self.hit_list = []
     for tile in tiles:
        if rect.colliderect(tile):
            self.hit_list.append(tile)    
     return self.hit_list    


    def checkColisionsx(self,rect,tiles,x_change):
         colisions = self.collision_test(rect,tiles)
         for tile in colisions:
             if (x_change > 0):
                 rect.x = tile.left - rect.w - 5
                 x_change = 0
             if (x_change < 0):
                 rect.x = tile.right + 5
                 x_change = 0    
        
    def checkColisionsy(self,rect,tiles,y_change):
         colisions = self.collision_test(rect,tiles)
         for tile in colisions:
             if (y_change < 0):
                 self.position.y = tile.bottom + 5
                 rect.y = self.position.y
                 y_change = 0
             if  (y_change > 0):
                 self.position.y = tile.top - rect.h - 5
                 rect.y = self.position.y    
                 y_change = 0

    def bomb_explosion(self,rect,tiles,x_change,y_change):
        pass             


    def update(self,rect,tiles,x_change,y_change):
        self.checkColisionsx(rect,tiles,x_change)
        self.checkColisionsy(rect,tiles,y_change)
        rect.x += x_change
        rect.y += y_change

    def clientParse(self):
        parser = argparse.ArgumentParser(description='Bomberman Game - Grupo 7')    

     ##########################################################   

    def show_text(self, text, size, color, x, y):
        #Show some text on the display
        font = pygame.font.Font(self.font,size) 
        text = font.render(text, True, color)
        text_rect = text.get_rect()   
        text_rect.midtop = (x,y)
        self.display.blit(text,text_rect)

    def show_inicial_logo(self,x,y):
        start_logo_rect = self.bomberman_logo.get_rect()    
        start_logo_rect.midtop = (x,y)
        self.display.blit(self.bomberman_logo,start_logo_rect) 

    def start_dipslay(self):
        self.show_inicial_logo(constants.WIDTH/2,60)
        self.show_text('PRESS SOME KEY TO PLAY!',28,constants.WHITE,constants.WIDTH/2,420)
        pygame.display.flip()
        self.waiting_for_players()

    def waiting_for_players(self):
        waiting = True
        while waiting:
            self.clock.tick(constants.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False 
                    self.running = False   
                if event.type == pygame.KEYUP:
                    waiting = False  

    def game_over_display(self):
        pass             


class Player():
    def __init__(self,rect,bombs,x_change,y_change):
        self.rect = rect
        self.bombs = bombs
        self.x_change = x_change
        self.y_change = y_change  

class Bomb():
    def __init__(self,x,y):
        self.x = x
        self.y = y


g = Game()
g.start_dipslay()                            

while g.running:
    g.new_game()
    g.game_over_display()

