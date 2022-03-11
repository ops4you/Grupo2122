import pygame
import constants
import chars
import os


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
    

    def new_game(self):
        #inicialize char classes
        self.all_chars = pygame.sprite.Group()
        self.run()

    def run(self):
        #game_loop
        self.playing = True
        while self.playing:
            self.clock.tick(constants.FPS)   
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
    
    def update_chars(self):
        #update chars
        self.all_chars.update()
        pygame.display.update()
        pass

    def draw_chars(self):
        #draw chars
        self.display.fill(constants.WHITE) #cleaning display
        self.all_chars.draw(self.display) #draw all chars
        pygame.display.flip()

    def load_files(self):
        #load image files
        image_path = os.path.join(os.getcwd(),'images')
        self.bomberman_logo = os.path.join(image_path,constants.LOGO)
        self.bomberman_logo = pygame.image.load(self.bomberman_logo)

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
    def __init__(self,x,y,bombs,x_update,y_update,bomb_update):
        self.x
        self.y
        self.bombs
        self.x_update
        self.y_update
        self.bomb_update

    def load_file(self):
        image_path = os.path.join(os.getcwd(),'images')
        self.bomberman = os.path.join(image_path,constants.BOMBERMAN)
        self.bomberman = pygame.image.load(self.bomberman)


    def events(self):
        #define game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False        
    
    def update(self):
        #update chars
        self.all_chars.update()
        pygame.display.update()
        pass

    def draw(self):
        #draw chars
        pygame.display.blit(self.bomberman)

    def run(self):
        #game_loop
        self.playing = True
        while self.playing:
            self.clock.tick(constants.FPS)   
            self.events()
            self.update()
            self.draw()   

    


g = Game()
g.start_dipslay()                            

while g.running:
    g.new_game()
    g.game_over_display()

