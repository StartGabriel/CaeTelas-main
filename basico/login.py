import pygame
import sys
import sqlite3

from basico.window import Window
from basico.button import Button
from basico.input import Input
import basico.tools as tools
import bdpython.user as user

pygame.init()
class Login():
    def __init__(self,
                 cnn:sqlite3.Connection):

        self.window_size = [1000,600]
        self.window_color = "black"
        self.window_background = "images/pantano.jpg"
        self.window = Window(self.window_size,self.window_color,self.window_background).pack()
        self.window_backup = self.window.copy()
        self.cnn = user.conectar(cnn)
        
        self.input_size = [400,50]
        self.input_coordinates = tools.get_obj_center(self.window_size,self.input_size)
        self.input_title = "LOGIN"
        self.input_color_title = "black"
        self.input_color = "white"
        
        self.button_size = [400,50]
        self.button_coordinates = [self.input_coordinates[0],self.input_coordinates[1]+self.button_size[1]+10]
        self.button_title = "RETORNAR"
        self.button_color_title = "white"
        self.button_color = "black"
        
        self.loop = True


    def pack(self):
        while self.loop:
            self.matricula = Input(window = self.window,
                            size= self.input_size,
                            coordinates= self.input_coordinates,
                            title= self.input_title,
                            color_title= self.input_color_title,
                            color= self.input_color)
            
            self.retornar = Button(window= self.window,
                                   title= self.button_title,
                                   size= self.button_size,
                                   color= self.button_color,
                                   coordinates= self.button_coordinates,
                                   command= self.back,
                                   color_title= self.button_color_title)
            
            self.retornar.pack()
            self.matricula.pack()
    
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if events.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.verify =self.matricula.run(pos=pos)
                    self.retornar.run(pos=pos)
                    pygame.display.flip()
                    self.loop = self.confirmed(self.verify)
                    self.matricula.clear_window()
            
            pygame.display.flip()
        self.window.blit(self.window_backup,(0,0))
        return self.verify

    def confirmed(self,matricula):
        try:
            self.window.blit(self.window_backup,(0,0))
            users =  user.consultar_user(conn=self.cnn, user_id=matricula)
            if users[0] == int(matricula):
                return False
            else: 
                return True
        except:
            return True
    
    def back(self):
        from main_menu import MainMenu
        self.app = MainMenu()
        self.app.run()