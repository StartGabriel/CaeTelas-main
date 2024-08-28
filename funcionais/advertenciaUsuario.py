import pygame
import sys

import basico.button as button
import basico.tools as tools

from basico.button import Button
from basico.input import Input
from basico.window import Window, DefauthWindow

import bdpython.user as User
import bdpython.adivertencia as advertencia

class Advertencia:
    def __init__(self):
        self.window = DefauthWindow()
        self.menu = Window(self.window.size,self.window.color, self.window.background).pack()
        self.__button = button.DefauthButton()
    
    def user(self):
        self.gerar_botoes()
        self.conectar()
        
    def conectar(self):
        self.cnn_user = User.conectar("bdpython/user.db")
        self.cnn_advertencia = User.conectar("bdpython/advertencia.db")
        
    def gerar_botoes(self):
        self.but_add = Button(window=self.menu,
                              title="ADICIONAR",
                              size=self.__button.size,
                              color=self.__button.color,
                              coordinates=[0,0],
                              command=self.incluir,
                              color_title=self.__button.color_title)
        self.but_remover = Button(window=self.menu,
                              title="REMOVER",
                              size=self.__button.size,
                              color=self.__button.color,
                              coordinates=[0,0],
                              command=self.excluir,
                              color_title=self.__button.color_title)
        self.inp_id = Input(window=self.menu,
                            size=self.__button.size,
                            coordinates=[0,0],
                            title="ID",
                            color=self.__button.color,
                            color_title=self.__button.color_title)
        self.buts = [self.but_add,self.but_remover]
        self.but_mid = tools.get_obj_center(self.window.size,self.__button.size)
        button.alight_buttons(self.but_mid,"y",10,self.buts)
        for but in self.buts:
            but.pack()
        self.main_loop()
    def incluir(self):
        self.validar()
    def excluir(self):
        self.validar
    
    def validar(self):
        button.alight_buttons(self.but_mid,"y",10,[self.buts[0],self.buts[1],self.inp_id])
        self.inp_id.pack()
        self.main_loop()
    def main_loop(self):
        self.loop = True
        while self.loop:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if events.type == pygame.MOUSEBUTTONDOWN:
                    self.pos = pygame.mouse.get_pos()
                    for but in self.buts:
                        but.run(self.pos)
                    self.id = self.inp_id.run(self.pos)
                    self.inp_id.clear_window()
                    
            pygame.display.flip()
        
