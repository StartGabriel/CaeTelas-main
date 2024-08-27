import pygame
import sys

import basico.button as button
import basico.tools as tools
from basico.button import Button
from basico.input import Input
from basico.window import Window
from bdpython import atendimentos
import funcionais.aviso as aviso

class Atendimento:
    def __init__(self,id:int = None):
        self.window_size= [1000,600]
        self.window_color= "black"
        self.window_background= "images/pantano.jpg"
        self.menu = Window(self.window_size,self.window_color,self.window_background).pack()
        
        self.but_size = [300,50]
        self.but_color = "white"
        self.but_color_title = "black"
        
        self.id = id
        
    def user(self):
        self.window_title = tools.insert_text("SOLICITAR ATENDIMENTO","white",50,"black")
        self.title_mid = tools.get_obj_center(self.window_size,self.window_title.get_size())
        self.menu.blit(self.window_title,(self.title_mid[0],10))
        self.conectar()
        self.botoes()
    
    
    def conectar(self):
        try:
            self.cnn =  atendimentos.conectar("bdpython/atendimentos.db")
            atendimentos.criar_tabela(self.cnn)
            
        except:
            pass
            

        
    def botoes(self):
        self.but_jogos = Button(window=self.menu,
                               title="JOGOS",
                               size=self.but_size,
                               color=self.but_color,
                               color_title=self.but_color_title,
                               coordinates=[0,0],
                               command=self.__jogos)

        self.but_reclamacoes = Button(window=self.menu,
                               title="RECLAMAÇÕES",
                               size=self.but_size,
                               color=self.but_color,
                               color_title= self.but_color_title,
                               coordinates=[0,0],
                               command=self.__reclamacoes)
        
        self.but_assistencia = Button(window=self.menu,
                               title="AJUDA",
                               size=self.but_size,
                               color=self.but_color,
                               color_title= self.but_color_title,
                               coordinates=[0,0],
                               command=self.__ajuda)

        self.but_voltar = Button(window=self.menu,
                               title="VOLTAR",
                               size=self.but_size,
                               color=self.but_color,
                               color_title= self.but_color_title,
                               coordinates=[0,0],
                               command=self.voltar)

        self.buts = [self.but_jogos, self.but_reclamacoes, self.but_assistencia, self.but_voltar]
        self.but_mid = tools.get_obj_center(self.window_size,self.but_size)
        button.alight_buttons(self.but_mid,"y",10, self.buts)
        
        for but in self.buts:
            but.pack()
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
            pygame.display.flip()
            
    def __jogos(self):
        self.inserir_solicitacao(1)
        
    
    def __reclamacoes(self):
        self.inserir_solicitacao(2)
    
    def __ajuda(self):
        self.inserir_solicitacao(3)
    
    def voltar(self):
        self.loop = False
        
    def inserir_solicitacao(self,id_solicitacao):
        atendimentos.inserir_solicitacoes(self.cnn,self.id,id_solicitacao, "não")
        self.aviso = aviso.Avisos(self.but_size,[0,0],"AVISO!","black","red")
        self.loop = self.aviso.mensagem("solicitação enviada com sucesso")
        
class Admin:
    def __init__(self):
        self.window_size = [1000,600]
        self.window_color= "black" 
        self.window_background = "images/pantano.jpg"
        self.menu = Window(self.window_size,self.window_color,self.window_background).pack()
        self.window_backup = self.menu.copy()
        self.but_size = [900,50]
        self.but_color = "white"
        self.but_colot_title = "black"
        self.but_mid = tools.get_obj_center(self.window_size,self.but_size)
        self.buts = []
        self.coordinate_init = 0
        self.page = 0
    def conectar(self):
        self.cnn = atendimentos.conectar("bdpython/atendimentos.db")
        
        
        
    def admin(self):
        self.conectar()
        self.consulta = atendimentos.consultar_todos(self.cnn)
        self.gerar_botoes()
        
    def gerar_botoes(self):
        self.buts = []
        self.coordinate_init = 10
        

        for dados in range(self.page,self.page+7):
            try:
                self.buts.append(Button(window=self.menu,
                                    title=f"SOLICITACÃO: {self.consulta[dados][0]}, ID: {self.consulta[dados][1]}, MOTIVO: {self.consulta[dados][2]}, CONCLUIDA: {self.consulta[dados][3]}",
                                    size=self.but_size,
                                    color=self.but_color,
                                    coordinates=self.but_mid,
                                    color_title=self.but_colot_title,
                                    command=self.check))
            except:
                pass
        for but in self.buts:
            but.coordinates = [but.coordinates[0],self.coordinate_init]
            self.coordinate_init = but.coordinates[1] + but.size[1] + 10
            but.pack()
        self.but_mid2 = tools.get_obj_center(self.window_size,[200,50])
        self.but_voltar = Button(window= self.menu,
                                 title= "SAIR",
                                 size= [200,50],
                                 color= "red",
                                 coordinates=[self.but_mid2[0]-210,550],
                                 command=self.sair,
                                 color_title= self.but_colot_title)
        
        self.but_next_page = Button(window= self.menu,
                                 title= "PROXIMA",
                                 size= [200,50],
                                 color= "green",
                                 coordinates=[self.but_mid2[0],550],
                                 command=self.next_page,
                                 color_title= self.but_colot_title)
        
        self.but_return_page = Button(window= self.menu,
                                 title= "VOLTAR",
                                 size= [200,50],
                                 color= "green",
                                 coordinates=[self.but_mid2[0]+210,550],
                                 command=self.return_page,
                                 color_title= self.but_colot_title)
        self.buts_control = [self.but_voltar,self.but_next_page,self.but_return_page]
        self.but_voltar.pack()
        self.but_next_page.pack()
        self.but_return_page.pack()
            
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
                    for index,but in enumerate(self.buts):
                        self.indexx= index
                        but.run(self.pos)
                    for buts in self.buts_control:
                        buts.run(self.pos)
                       
            pygame.display.flip()
    
    def check(self):
        print("Botão clicado")
        self.indes = self.indexx + 1 + self.page
        print(f"ID do botão: {self.indes}")
        print(f"Status atual: {self.consulta[self.indes][3]}")
        
        if self.consulta[self.indes][3] == "sim":
            print("entrou no sim")
            atendimentos.atualizar_user(self.cnn, self.indes, atendido="não")
            print(f"{self.consulta[self.indes][3]}")
        elif self.consulta[self.indes][3] == "não":
            print("entrou no nao")
            atendimentos.atualizar_user(self.cnn, self.indes, atendido="sim")
        
        self.update_page()

        
        
    def update_page(self):
        self.menu.blit(self.window_backup, (0, 0))  
        pygame.display.flip()
        self.admin()


    
    def sair(self):
        from atendimento import AtendimentoTela
        self.app = AtendimentoTela()
        self.app.run()
        
    def next_page(self):
        self.page+=7
        self.update_page()
    def return_page(self):
        self.page-=7
        self.update_page()
