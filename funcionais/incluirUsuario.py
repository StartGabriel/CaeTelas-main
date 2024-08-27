import pygame
import sys
import re
import sqlite3

import basico.tools as tools
import bdpython.user as user
import basico.button as button
from basico.button import Button
from basico.window import Window
from basico.input import Input
pygame.init()

class Incluir:
    def __init__(self):
        self.window_size = [1000,600]
        self.window_color = "black"
        self.window_background = "images/pantano.jpg"
        self.menu = Window(self.window_size,self.window_color,self.window_background).pack()
        self.window_backup = self.menu.copy()
        
        self.but_size = [300,50]
        self.but_color = "white"
        self.but_color_title = "black"
        self.but_mid = tools.get_obj_center(self.window_size,self.but_size)

        self.retorna = []

    def user(self):
        self.gerar_botoes()
        self.main_loop()
        self.incluir(self.retorna[0],self.retorna[1],self.retorna[2])
    def gerar_botoes(self):
        self.nome = Input(window=self.menu,
                          size=self.but_size,
                          coordinates=[0,0],
                          title="nome",
                          color=self.but_color,
                          color_title=self.but_color_title,)
        self.idade = Input(window=self.menu,
                           size=self.but_size,
                           coordinates=[0,0],
                           title="idade",
                           color=self.but_color,
                           color_title=self.but_color_title,)
        
        self.email = Input(window=self.menu,
                           size=self.but_size,
                           coordinates=[0,0],
                           title="email",
                           color=self.but_color,
                           color_title=self.but_color_title,)
        self.inputs = [self.nome, self.idade, self.email]
        self.buts_input = [self.nome,self.idade,self.email]
        button.alight_buttons(self.but_mid,"y",10,self.buts_input)
        
    def main_loop(self):
        for inp in self.inputs:
            inp.pack()
            self.loop = True
            while self.loop:
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if events.type == pygame.MOUSEBUTTONDOWN:
                        self.pos = pygame.mouse.get_pos()
                        self.retorna.append(inp.run(self.pos))
                        inp.clear_window()
                        self.loop = False
                pygame.display.flip()

    def incluir(self, nome: str, idade: int, email: str, bd="bdpython/user.db"):
        from funcionais.aviso import Avisos
        try:
            nome = self.tratar_entrada(nome)
            cnn = user.conectar(bd)
            user.criar_tabela(cnn)
            user.inserir_user(cnn, nome=nome, idade=idade, email=email)
            
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.erro = Avisos(size_button=[300, 50],
                                                coordinates_button=[0,0],
                                                title_button="Erro",
                                                color_button="black",
                                                color_title="red")
            self.erro.mensagem(f"Erro inesperado: {str(e)}",
                               size_text_message=30,color="yellow")
        finally:
            from atendimento import AtendimentoTela
            app = AtendimentoTela()
            app.run()
        

    def tratar_entrada(self, entrada):
        try:
            tratado = re.sub(r'[^a-zA-Z\s]', '', entrada)
            return tratado
        except Exception as e:
            print(f"Erro ao tratar entrada: {e}")
            raise  # Relevanta a exceção após o log para que ela possa ser capturada na chamada
