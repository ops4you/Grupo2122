#Player class
class Player():
    def __init__(self,ip_port,rect,bombs,x_change,y_change):
        self.ip_port = ip_port
        self.rect = rect
        self.bombs = bombs
        self.x_change = x_change
        self.y_change = y_change  

#Bomb class
class Bomb():
    def __init__(self,x,y):
        self.x = x
        self.y = y
