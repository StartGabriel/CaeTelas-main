import pygame
import sys

import basico.button as button
import basico.tools as tools
import basico.login as login


from basico.button import Button
from basico.input import Input
from basico.window import Window

import main_menu

pygame.init()

class AtendimentoTela:
    def __init__(self):
        self.__title = tools.insert_text(text="ATENDIMENTO",
                                       color="white",
                                       size= 75,
                                       background_color="black")
        self.__menu = Window(size=[1000, 600], color="black", background="images/pantano.jpg").pack()
        self.__center_title = tools.get_obj_center([1000,600],self.__title.get_size())
        self.__menu.blit(self.__title,[self.__center_title[0],0])
        self.__window_backup = self.__menu.copy()
        self.__botoes = self.__tela_botoes()

    def __incluir(self):
        from funcionais.incluirUsuario import Incluir
        incluindo = Incluir()
        incluindo.user()

    def __alterar(self):
        from funcionais.alterarUsuario import Alterar
        alterando = Alterar()
        alterando.user()

    def __excluir(self):
        from funcionais.excluirUsuario import Excluir
        excluindo = Excluir()
        excluindo.user()

    def __consultar_atendimento(self):
        from funcionais.consultarUsuario import ConsultarDados
        consultar = ConsultarDados()
        consultar.user()
        
    def __voltar(self):
        run = main_menu.MainMenu()
        run.run()

    def __consultar_solicitacoes(self):
        from funcionais.atendimentoUsuario import Admin
        atd = Admin()
        atd.admin()

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
        but_excluir = Button(window=self.__menu,
                             title="excluir",
                             size=[400, 50],
                             color=None,
                             coordinates=[0, 0],
                             command=self.__excluir,
                             color_title="black",
                             background="images/placa.webp",
                                            size_title=50)
        
        but_consultar_atendimento = Button(window=self.__menu,
                                           title="consultar",
                                           size=[400, 50],
                                           color=None,
                                           coordinates=[0, 0],
                                           command=self.__consultar_atendimento,
                                           color_title="black",
                                           background="images/placa.webp",
                                            size_title=50)
        but_consultar_solicitacoes = Button(window=self.__menu,
                                           title="solicitações",
                                           size=[400, 50],
                                           color=None,
                                           coordinates=[0, 0],
                                           command=self.__consultar_solicitacoes,
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
        
        
        botoes = [but_consultar_atendimento, but_alterar, but_excluir, but_incluir, but_consultar_solicitacoes, but_voltar]
        centro_x = button.get_center_button([1000, 600], but_incluir, "j")
        button.alight_buttons([centro_x[0],150], "y", 10, botoes)
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
            pygame.display.flip()

if __name__ == "__main__":
    app = AtendimentoTela()
    app.run()
