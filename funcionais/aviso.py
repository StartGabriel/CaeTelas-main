import sys
import pygame
from typing import List

# Importações do seu projeto
from basico.input import Input
import bdpython.user
import basico.tools as tools
import basico.window
from basico.button import Button
from usuario import UsuarioTela
import basico.button as button

pygame.init()

class Avisos:
    def __init__(self,
                 size_button: List[int],
                 coordinates_button: List[int],
                 title_button: str,
                 color_button: str,
                 color_title: str):
        """
        Inicializa a classe Avisos com os parâmetros fornecidos.
        
        :param size_button: Tamanho do botão.
        :param coordinates_button: Coordenadas do botão.
        :param title_button: Título do botão.
        :param color_button: Cor do botão.
        :param color_title: Cor do título do botão.
        """
        self.menu = basico.window.Window([1000, 600], "black", "images/pantano.jpg").pack()
        self.size = size_button
        self.coordinates = coordinates_button
        self.backups = self.menu.copy()
        self.title = title_button
        self.color = color_button
        self.color_title = color_title
        self.loops = True
        self.verify = None

        self.text_title = tools.insert_text(text=self.title,
                                                   color=self.color_title,
                                                   size=self.size[1],
                                                   background_color=self.color)
        self.coordinates_title = tools.get_obj_center([1000, 600], self.text_title.get_size())
        self.menu.blit(self.text_title, [self.coordinates_title[0], 0])

    def excluir(self, nome: str, text: str) -> bool:
        """
        Exibe a mensagem de exclusão e os botões de confirmação.

        :param nome: Nome do usuário a ser excluído.
        :param text: Texto de aviso.
        :return: Retorna True se confirmado, False caso contrário.
        """
        self.excluindo = nome
        self.__text_aviso = tools.insert_text(text=f"{text} {nome}?",
                                                     color=self.color_title,
                                                     size=self.size[1],
                                                     background_color=self.color)

        self.coordinates_text = tools.get_obj_center([1000, 600], self.__text_aviso.get_size())
        self.menu.blit(self.__text_aviso, (self.coordinates_text[0],self.coordinates_text[1]-50))
        self.create_confirmation_buttons(coordinates_first_button=[self.coordinates_text[0], self.coordinates_text[1] + 140],
                                         coordinates_second_button=[self.coordinates_text[0] + self.__text_aviso.get_size()[0] - 100,self.coordinates_text[1] + 140],
                                         align="x")
        self.run_event_loop(self.botoes)
        return self.verify

    def mensagem(self, text: str,size_text_message:int=25,color:str = "red") -> None:
        """
        Exibe uma mensagem de aviso e um botão para retornar.

        :param text: Texto da mensagem.
        :param size_text_message: tamanho da fonte
        :param color: cor da fonte
        """
        self.__text_aviso = tools.insert_text(text=text,
                                                     color=color,
                                                     size=size_text_message,
                                                     background_color=self.color)
        self.coordinates_text = tools.get_obj_center([1000, 600], self.__text_aviso.get_size())
        self.menu.blit(self.__text_aviso, self.coordinates_text)

        self.coordinates_return = [self.coordinates_text[0] + self.__text_aviso.get_size()[0] / 2 - 150,
                                   self.coordinates_text[1] + 70]
        self.but_return = Button(window=self.menu,
                                 title="RETORNAR",
                                 size=[300, 50],
                                 color="red",
                                 coordinates=self.coordinates_return,
                                 command=self.note)
        self.but_return.pack()
        self.this_return = self.run_event_loop([self.but_return])
        return False

    def create_confirmation_buttons(self,
                                    coordinates_first_button:list = [0,0],
                                    coordinates_second_button:list = [0,0],
                                    align:str = "x") -> None:
        """
        Cria os botões de confirmação para exclusão.
        """
        self.but_yes = Button(window=self.menu,
                              title="SIM",
                              size=[100, 50],
                              color="red",
                              coordinates=coordinates_first_button,
                              command=self.yes,
                              size_title=50)

        
        self.but_not = Button(window=self.menu,
                              title="NÃO",
                              size=[100, 50],
                              color="green",
                              coordinates=coordinates_second_button,
                              command=self.note,
                              size_title=50)
        self.mid_confirmation = tools.get_obj_center(self.menu.get_size(),self.but_not.size)
        self.botoes = [self.but_yes, self.but_not]
        button.alight_buttons(self.mid_confirmation,"x",10,self.botoes)
        
        
        self.but_yes.pack()
        self.but_not.pack()
        self.run_event_loop(self.botoes)
        return self.verify

    def run_event_loop(self, buttons: List[Button]) -> None:
        """
        Executa o loop de eventos do Pygame.

        :param buttons: Lista de botões a serem verificados no loop.
        """
        while self.loops:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for button in buttons:
                        button.run(pos)
            pygame.display.flip()

    def yes(self) -> None:
        """
        Confirma a exclusão.
        """
        self.loops = False
        self.verify = True
        return True

    def note(self) -> None:
        """
        Cancela a exclusão.
        """
        self.loops = False
        self.verify = False
        return False

# Exemplo de uso:

