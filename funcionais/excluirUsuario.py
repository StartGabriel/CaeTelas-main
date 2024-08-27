import sys
import pygame
from typing import List

import bdpython.user
import basico.tools as tools
from basico.window import Window
from basico.input import Input



pygame.init()

class Excluir:
    def __init__(self):
        """
        Inicializa a classe Excluir.
        
        """
        self.window_size = [1000,600]
        self.window_color= "black"
        self.window_background= "images/pantano.jpg"
        self.menu = Window(self.window_size,self.window_color,self.window_background).pack()
        
        self.but_size= [300,50]
        self.but_color= "white"
        self.but_color_title= "black"
        self.window_backups= self.menu.copy()
        
       

    def user(self) -> None:
        """
        Configura o botão de entrada e inicia o loop do evento.
        """
        self.but_mid= tools.get_obj_center(self.window_size,self.but_size)
        self.consulta = Input(window=self.menu,
                              size=self.but_size,
                              coordinates= self.but_mid,
                              title="id",
                              color=self.but_color,
                              color_title=self.but_color_title)
        self.consulta.pack()
        self.excluindo =self.main_loop()
        self.excluir(self.excluindo)
        self.sair()
        
    def main_loop(self):
        self.loop = True
        while self.loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pos= pygame.mouse.get_pos()
                    self.retorna= self.consulta.run(self.pos)
                    return self.retorna
            pygame.display.flip()
    print("saiu do loop")


    def excluir(self, user_id: int, db_path: str = "bdpython/user.db") -> None:
        """
        Exclui um usuário do banco de dados.

        :param user_id: O ID do usuário a ser excluído.
        :param db_path: O caminho do banco de dados.
        """
        from funcionais.aviso import Avisos
        try:
            conn = bdpython.user.conectar(db_path)
            user_data = bdpython.user.consultar_user(conn, user_id)
            if not user_data:
                self.show_message(f"'{user_id}' User não encontrado")
                return

            user_name = user_data[1]
            confirmacao = Avisos([300, 50], [275, 0], "AVISO!", "black", "white")
            confirmed = confirmacao.excluir(user_name, "Deseja excluir")

            if confirmed:
                self.deletar_usuario(conn, user_id, user_name)
            else:
                self.show_message("Operação de exclusão cancelada.")
        except Exception as e:
            self.show_message(f"Erro ao excluir o usuário: {e}")
        pygame.display.flip()
        

    def deletar_usuario(self, conn, user_id: int, user_name: str) -> None:
        """
        Deleta um usuário do banco de dados e exibe uma mensagem de confirmação.

        :param conn: A conexão com o banco de dados.
        :param user_id: O ID do usuário a ser excluído.
        :param user_name: O nome do usuário a ser excluído.
        """
        bdpython.user.deletar_user(conn, user_id)
        self.show_message(f"user '{user_name}' deletado")

    def show_message(self, message: str) -> None:
        """
        Exibe uma mensagem de aviso.

        :param message: A mensagem a ser exibida.
        """
        from funcionais.aviso import Avisos
        aviso_mensagem = Avisos([300, 50], [275, 0], "AVISO!", "black", "white")
        self.loop= aviso_mensagem.mensagem(message)
        print(self.loop)
        print("ta no loop")
        

    def sair(self):
        self.loop = False
        from atendimento import AtendimentoTela
        self.app = AtendimentoTela()
        self.app.run()

