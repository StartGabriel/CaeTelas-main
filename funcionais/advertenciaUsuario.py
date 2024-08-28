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
        advertencia.criar_tabela(self.cnn_advertencia)
        
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
        
        self.but_consultar = Button(window=self.menu,
                              title="CONSULTAR",
                              size=self.__button.size,
                              color=self.__button.color,
                              coordinates=[0,0],
                              command=self.consultar,
                              color_title=self.__button.color_title)
        self.but_input= Input(window=self.menu,
                            size=self.__button.size,
                            coordinates=[self.but_mid[0],500],
                            title="ID",
                            color=self.__button.color,
                            color_title=self.__button.color_title)
        
        self.buts = [self.but_add,self.but_remover,self.but_consultar]
        button.alight_buttons(self.but_mid,"y",10,self.buts)
        for but in self.buts:
            but.pack()
        self.main_loop()
        
    def incluir(self):
        self.get_id()
        self.veryfi = self.validar(self.id)
        if self.veryfi == True:
            self.confirmar()
            if self.confirmado == True:
                self.get_motivo()
                advertencia.inserir_advertencia(self.cnn_advertencia,self.id,self.motivo)
        self.sair()
        
    def excluir(self):
        self.get_id()
        advertencia.deletar_advertencia(self.cnn_advertencia,self.id)
    
    def consultar(self):
        self.get_id()
        from funcionais.aviso import Avisos
        self.nr_adivertencia = advertencia.consultar_adivertencia(self.cnn_advertencia,self.id)
        if self.nr_adivertencia:
            self.user_adivertencia = User.consultar_user(self.cnn_user, self.nr_adivertencia[0][1])
            self.consultado = Avisos(self.__button.size,[self.but_mid[0],10],"USER CONSULTADO","black","gold")
            self.consultado.mensagem(f"NÚMERO: {self.id}, ALUNO: {self.user_adivertencia[1]}, MOTIVO: {self.nr_adivertencia[0][2]}")
        else:
            self.consultado = Avisos(self.__button.size,[self.but_mid[0],10],"USER CONSULTADO","black","gold")
            self.consultado.mensagem(f"ID {self.id} NÃO ENCONTRADO OU REMOVIDO")
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
    def validar(self,id):
        from funcionais.aviso import Avisos
        self.id_consulta= User.consultar_user(self.cnn_user,id)
        if self.id_consulta is not None:
            return True
        
        else:
            self.false = Avisos(self.__button.size,[self.but_mid[0],10],"ERRO","black","gold")
            self.false.mensagem(f"user id: {id} NOT FOUND")
            self.sair()
        
    def confirmar(self):
        from funcionais.aviso import Avisos
        self.confirmado = Avisos(self.__button.size,[self.but_mid[0],10],"CONFIRMAR","black","gold")
        self.title_confirmation = tools.insert_text(text=f"adicionar advertencia ao id:{self.id} nome:{self.id_consulta[1]}",
                                                    color="olive",
                                                    size=30,
                                                    background_color="black")
        self.title_confirmation_mid = tools.get_obj_center(self.window.size,self.title_confirmation.get_size())
        self.menu.blit(self.title_confirmation,(self.title_confirmation_mid[0],200))
        pygame.display.flip()
        self.confirmado = self.confirmado.create_confirmation_buttons()
        print(self.confirmado)
        
        
    def sair(self):
        from atendimento import AtendimentoTela
        self.app = AtendimentoTela()
        self.app.run()