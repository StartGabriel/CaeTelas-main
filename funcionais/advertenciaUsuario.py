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
        self.conectar()
        self.gerar_botoes()
        self.sair()
        
    def conectar(self):
        self.cnn_user = User.conectar("bdpython/user.db")
        self.cnn_advertencia = advertencia.conectar("bdpython/advertencia.db")
        
    def gerar_botoes(self):
        self.but_mid = tools.get_obj_center(self.window.size,self.__button.size)
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
        
        self.but_input= Input(window=self.menu,
                            size=self.__button.size,
                            coordinates=[self.but_mid[0],400],
                            title="ID",
                            color=self.__button.color,
                            color_title=self.__button.color_title)
        
        self.buts = [self.but_add,self.but_remover]
        button.alight_buttons(self.but_mid,"y",10,self.buts)
        for but in self.buts:
            but.pack()
        self.main_loop()
        
    def incluir(self):
        self.get_id()
        self.get_motivo()
        advertencia.inserir_advertencia(self.cnn_advertencia,self.id,self.motivo)
        
    def excluir(self):
        self.get_id()
        advertencia.deletar_advertencia(self.cnn_advertencia,self.id)
    
    def get_id(self):
        self.but_input.pack()
        self.id = self.loop_input()

        
    def get_motivo(self):
        self.inp_mid = tools.get_obj_center(self.window.size,[700,50])
        self.but_input = Input(window=self.menu,
                            size=[700,50],
                            coordinates=[self.inp_mid[0],400],
                            title="MOTIVO",
                            color=self.__button.color,
                            color_title=self.__button.color_title)
        self.but_input.pack()
        self.motivo = self.loop_input()
        
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

                    
            pygame.display.flip()
        self.but_input.clear_window()
        return self.retornar
                    
    def loop_input(self): #gambiarra provisória, ou não
        self.loop = True
        while self.loop:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if events.type == pygame.MOUSEBUTTONDOWN:
                    self.pos = pygame.mouse.get_pos()
                    self.retornar = self.but_input.run(self.pos)
                    self.loop=False
            pygame.display.flip()
        return self.retornar

    def sair(self):
        from atendimento import AtendimentoTela
        self.app = AtendimentoTela()
        self.app.run()