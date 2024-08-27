import basico.button as button
from basico.button import Button
from basico.input import Input
import basico.window as window
from basico.window import Window
import basico.tools as tools
import pygame
import sys
import basico.login as login
import funcionais.consultarUsuario

import funcionais.atendimentoUsuario as atendimentoUsuario

import funcionais.alterarUsuario as alterarUsuario
import funcionais.incluirUsuario
import main_menu

pygame.init()

class UsuarioTela:
    def __init__(self):
        self.__title = tools.insert_text(text="USUARIO",
                                       color="white",
                                       size= 75,
                                       background_color="black")
        self.__logon = login.Login("bdpython/user.db").pack()
        self.__menu = Window(size=[1000, 600], color="black", background="images/pantano.jpg").pack()
        self.__center_title = tools.get_obj_center([1000,600],self.__title.get_size())
        self.__menu.blit(self.__title,[self.__center_title[0],0])
        self.__window_backup = self.__menu.copy()
        self.__botoes = self.__tela_botoes()
        
    def __incluir(self):
        incluindo = funcionais.incluirUsuario.Incluir(menu=self.__menu,
                                               size_button=[400, 50],
                                               coordinates_button=[300, 450],
                                               color_button="black",
                                               color_title="white")
        incluindo.user()
        
    def __alterar(self):
        alterando = alterarUsuario.Alterar()
        alterando.id = self.__logon
        alterando.user()

    def __atendimento(self):
        selecionar_atendimento = atendimentoUsuario.Atendimento(self.__logon)
        selecionar_atendimento.user()

    def __consultar_dados(self):
        consultar = funcionais.consultarUsuario.ConsultarDados()
        consultar.id = self.__logon
        consultar.user()

    def __consultar_todos(self):
        print("but_consultarTodos")
        
    def __voltar(self):
        run = main_menu.MainMenu()
        run.run()


    def __tela_botoes(self):
        but_incluir = Button(window=self.__menu,
                             title="incluir",
                             size=[400, 50],
                             color=None,
                             coordinates=[0, 0],
                             command=self.__incluir,
                             color_title="black",
                             background="images/placa.webp",
                                            size_title=50)
        but_alterar = Button(window=self.__menu,
                             title="alterar",
                             size=[400, 50],
                             color=None,
                             coordinates=[0, 0],
                             command=self.__alterar,
                             color_title="black",
                             background="images/placa.webp",
                                            size_title=50)
        but_atendimento = Button(window=self.__menu,
                             title="atendimento",
                             size=[400, 50],
                             color=None,
                             coordinates=[0, 0],
                             command=self.__atendimento,
                             color_title="black",
                             background="images/placa.webp",
                                            size_title=50)
        but_consultar_atendimento = Button(window=self.__menu,
                                           title="consultar",
                                           size=[400, 50],
                                           color=None,
                                           coordinates=[0, 0],
                                           command=self.__consultar_dados,
                                           color_title="black",
                                           background="images/placa.webp",
                                            size_title=50)
        but_voltar = Button(window=self.__menu,
                                     title="voltar",
                                     size=[400, 50],
                                     color=None,
                                     coordinates=[0, 0],
                                     command=self.__voltar,
                                     color_title="black",
                                     background="images/placa.webp",
                                            size_title=50)
        

        botoes = [but_consultar_atendimento, but_alterar, but_atendimento, but_incluir, but_voltar]
        centro_x = button.get_center_button([1000, 600], but_incluir, "j")
        button.alight_buttons([centro_x[0], 150], "y", 10, botoes)
        for botao in botoes:
            botao.pack()
        return botoes

    def run(self):
        loop = True
        while loop:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if events.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for run in self.__botoes:
                        run.run(pos)
                for tg in self.__botoes:
                    pos_tg = pygame.mouse.get_pos()
                    tg.tags_run(pos=pos_tg,
                                color_rect_point=None,
                                size_rect_point=[20,20],
                                background_point="images/seta_rosa.png")
            pygame.display.flip()

if __name__ == "__main__":
    app = UsuarioTela()
    app.run()
