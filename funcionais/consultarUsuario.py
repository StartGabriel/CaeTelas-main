from basico.input import Input
from basico.window import Window
import basico.tools as tools
import bdpython.user as user
import funcionais.aviso as aviso
import pygame
import sys
pygame.init()
class ConsultarDados:
    
    def __init__(self,window:pygame.Surface=None):
        self.size_window = [1000,600]
        self.background_window = "images/pantano.jpg"
        self.menu = Window(size= self.size_window, color="white", background= self.background_window).pack()
        self.window_backup = self.menu.copy()
        self.size_input = [300,50]
        self.title_input = "ID"
        self.color_input = "black"
        self.color_title_input = "white"
        self.mid_input = tools.get_obj_center(self.size_window,self.size_input)
        self.db_path = "bdpython/user.db"
        self.text_title = "INSIRA"
        self.color_title = "yellow"
        self.color_backgroud_title = "black"
        self.size_title = 50
        self.coordinate_title = None
        self.id = None
    def user(self):
        if self.id is not None:
            self.consultar(self.id)
        else:
            self.get_id()
            self.user()
            self.sair()
    def get_id(self):
            self.title = tools.insert_text(text=self.text_title,color=self.color_title,size=self.size_title,background_color=self.color_backgroud_title)
            self.coordinate_title = tools.get_obj_center(self.size_window,self.title.get_size())
            self.coordinate_title = [self.coordinate_title[0],10]
            self.menu.blit(self.title,self.coordinate_title)
            self.input_id = Input(window=self.menu,
                            size=self.size_input,
                            coordinates=self.mid_input,
                            title=self.title_input,
                            color= self.color_input,
                            color_title=self.color_title_input)
            self.input_id.pack()
            self.id = self.loop()
            self.atendimento = True
            
    def loop(self):
        self.loops = True
        while self.loop:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if events.type == pygame.MOUSEBUTTONDOWN:
                    self.pos = pygame.mouse.get_pos()
                    self.retorna = self.input_id.run(self.pos)
                    self.input_id.clear_window()
                    self.loops = False
                    return self.retorna
            pygame.display.flip()
            
    def consultar(self,id:int):
        try:
            self.conn = user.conectar(self.db_path)
            user_data = user.consultar_user(self.conn, id)
            if not user_data:
                self.nao_encontrado = aviso.Avisos([300, 50], [275, 0], "AVISO!", "black", "white")
                self.nao_encontrado.mensagem(f"'{id}' User não encontrado")
                return

            self.user_name = user_data[1]
            self.exibir(user_data=user_data)
            
        except:
            pass
    def exibir(self,user_data):
        self.exibindo = aviso.Avisos([300,50], [275,0],"USER","black","red")
        self.verify = self.exibindo.mensagem(f"Nome: {user_data[1]}, Idade: {user_data[2]}, E-mail: {user_data[3]}")
        if self.verify == False:
            self.sair()
    def sair(self):
        self.menu.blit(self.window_backup,(0,0))
        self.loops = False
    
        if self.atendimento == True: #gambiarra temporaria, ou não
            from atendimento import AtendimentoTela
            self.app = AtendimentoTela()
            self.app.run()