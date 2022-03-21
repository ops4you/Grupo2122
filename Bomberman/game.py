import pygame
import constants
import chars
import os

map1 ="""                             
                             
wwwwwwwwwwwwwwwwwwwwwwwwwwwww
w             w             w
w                           w
w    wwwwww    wwwww      www
www    w                  w w
w      w          w         w
w   wwwww     wwwwwww      ww
w      wwwwww     w     w   w
w    w      w   www  wwww   w
w      w          w     w   w
w   wwwwww www wwww     w   w
w     w              ww w   w
w                           w
wwwwwwwwwwwwwwwwwwwwwwwwwwwww"""

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
        self.p1 = Player(50,50,2,0,0)
        self.b1 = Bomb(0,0)
        self.pressb = -5000000000
        self.presse = -5000000000
        self.current_time = 0
        self.map1 = map1.splitlines()
    

    def new_game(self):
        #inicialize char classes
        self.all_chars = pygame.sprite.Group()
        self.run()

    def run(self):
        #game_loop
        self.playing = True
        while self.playing:
            self.clock.tick(constants.FPS)  
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
                  if(self.p1.x > 1):
                    self.p1.x_change = -2
                  else: self.p1.x_change = 0 
                if event.key == pygame.K_RIGHT:
                  if(self.p1.x < 433):
                     self.p1.x_change = 2
                  else: self.p1.x_change = 0
                if event.key == pygame.K_UP:
                 self.p1.y_change = -2
                if event.key == pygame.K_DOWN:
                 self.p1.y_change = 2
                if event.key == pygame.K_SPACE: 
                    if(self.p1.bombs>0):
                         self.pressb = pygame.time.get_ticks()
                         self.b1.x = self.p1.x
                         self.b1.y = self.p1.y
                         self.p1.bombs -= 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                 self.p1.x_change = 0  
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                 self.p1.y_change = 0                
    
    def update_chars(self):
        #update chars
        self.p1.update()
        print(self.p1.x,self.p1.y)
        pygame.display.update()

    def draw_chars(self):
        #draw chars
        self.display.fill(constants.WHITE) #cleaning display
        
        self.tiles(self.map1)
        self.display.blit(self.bomberman,(self.p1.x,self.p1.y))

        if (self.current_time - self.pressb)<3000:
            self.display.blit(self.bomb,(self.b1.x,self.b1.y))
        elif((self.current_time - self.pressb)>3000): 
            pygame.transform.flip(self.bomb,self.b1.x,self.b1.y)   
  
        pygame.display.flip()

    def load_files(self):
        #load image files
        image_path = os.path.join(os.getcwd(),'images')

        self.bomberman_logo = os.path.join(image_path,constants.LOGO)
        self.bomberman_logo = pygame.image.load(self.bomberman_logo)

        self.bomberman = os.path.join(image_path,constants.BOMBERMAN)
        self.bomberman = pygame.image.load(self.bomberman)

        self.bomb = os.path.join(image_path,constants.BOMB)
        self.bomb = pygame.image.load(self.bomb)

        #self.explode = os.path.join(image_path,constants.EXPLODE)
        #self.explode = pygame.image.load(self.explode)

        self.wall = os.path.join(image_path,constants.WALL) 
        self.wall = pygame.image.load(self.wall)

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

    def tiles(self,map1):
     for y, line in enumerate(self.map1):
        for x, c in enumerate(line):
            if c == "w":
                self.display.blit(self.wall, (x * 30, y * 30))


class Player():
    def __init__(self,x,y,bombs,x_change,y_change):
        self.x = x
        self.y = y
        self.bombs = bombs
        self.x_change = x_change
        self.y_change = y_change   
    
    def update(self):
        #update chars
        self.x += self.x_change
        self.y += self.y_change
        pygame.display.update()

class Bomb():
    def __init__(self,x,y):
        self.x = x
        self.y = y

g = Game()
g.start_dipslay()                            

while g.running:
    g.new_game()
    g.game_over_display()

