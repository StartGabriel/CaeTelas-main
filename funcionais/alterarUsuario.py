import pygame
import sys
import re

from basico.input import Input
from basico.button import Button
from basico.window import Window

import bdpython.user as user
import funcionais.aviso as aviso
import basico.button as button
import basico.tools as tools

import usuario


pygame.init()

class Alterar:
    def __init__(self):
        self.window_size = [1000,600]
        self.window_color = "black"
        self.window_background = "images/pantano.jpg"
        self.menu = Window(self.window_size, self.window_color, self.window_background).pack() #esse é o menu <-
        self.window_backup = self.menu.copy()
        
        self.window_title = "ALTERAR DADOS"
        self.window_title_color = "white"
        self.window_title_size = 50
        self.window_title_background_color = "black"
        
        self.inputs_color = "black"
        self.inputs_color_title= "white"
        self.inputs_coordinate = [0,0]
        
        self.buttons_size = [300,50]
        self.space = 10
        
        self.db_path = "bdpython/user.db"
        
        self.nome = None
        self.idade = None
        self.email = None
        
        self.verify = False
        self.cancelar = False
        self.loops = True
        self.id = None

    def user(self):
        if self.id is not None:
            self.gerar_titulo()
            self.botoes()
            self.confirmar()
            self.user_id = self.id
            if self.verify == True and self.cancelar == False:
                self.conectar()
                self.atualizar(cnn=self.conn,nome=self.nome, idade=self.idade,email= self.email)
            
        else:
            self.get_id()
            self.sair_atendimento()
    def get_id(self):
            self.id_title = "ID"
            self.id_color = "white"
            self.id_color_title = "black"
            self.id_mid = tools.get_obj_center(self.window_size,self.buttons_size)
            self.input_id = Input(window=self.menu,
                            size=self.buttons_size,
                            coordinates=self.id_mid,
                            title=self.id_title,
                            color=self.id_color,
                            color_title=self.id_color_title)
            self.input_id.pack()
            
            self.alterando = self.input_id
            self.id = self.coletar()
            self.user()
            
                
    def gerar_titulo(self):
            self.title_window = tools.insert_text(text= self.window_title,
                                                color= self.window_title_color,
                                                size= self.window_title_size,
                                                background_color= self.window_title_background_color)
            
            self.title_mid = tools.get_obj_center(self.window_size, self.title_window.get_size())
            self.menu.blit(self.title_window,(self.title_mid[0],self.space))
            self.window_backup2 = self.menu.copy()
            
    def conectar(self):
            try:
                self.conn = user.conectar(self.db_path)
                user_data = user.consultar_user(self.conn, self.user_id)
                if not user_data:
                    self.nao_encontrado = aviso.Avisos(self.buttons_size, [275, 0], "AVISO!", "black", "white")
                    self.nao_encontrado.mensagem(f"'{self.user_id}' User não encontrado")
                    return

                self.user_name = user_data[1]
                self.menu.blit(self.window_backup2,(0,0))
                
            except:
                pass
        
        
    def botoes(self):
        self.mid = tools.get_obj_center(coordinate_size=self.window_size,size_objt=self.buttons_size)
        self.but_nome = Button(window=self.menu,
                               title="NOME",
                               size=self.buttons_size,
                               color= "red",
                               coordinates=[0,0],
                               command=self.__alterar_nome)
        
        self.but_idade = Button(window=self.menu,
                               title="IDADE",
                               size=self.buttons_size,
                               color= "red",
                               coordinates=[0,0],
                               command=self.__alterar_idade)
        
        self.but_email = Button(window=self.menu,
                               title="E-MAIL",
                               size=self.buttons_size,
                               color= "red",
                               coordinates=[0,0],
                               command=self.__alterar_email)
        
        self.but_sair = Button(window=self.menu,
                               title="SAIR",
                               size=self.buttons_size,
                               color="green",
                               coordinates=[0,0],
                               command=self.sair)
        
        self.buts = [self.but_nome, self.but_idade, self.but_email, self.but_sair]
        button.alight_buttons(start_coordinates=self.mid,
                              orientation="y",
                              space=self.space,
                              buttons=self.buts)
        for but in self.buts:
            but.pack()
        pygame.display.flip()
        self.loop()
        
    def __alterar_nome(self):
        self.nome = Input(window=self.menu,
                          size=[600,50],
                          coordinates= self.inputs_coordinate,
                          title="nome",
                          color=self.inputs_color,
                          color_title=self.inputs_color_title)
        self.ajuste_coordenada(self.but_email.coordinates,self.but_email.size,self.space,self.nome)
        self.nome.pack()
        self.alterando = self.nome
        self.nome = self.coletar()
        
        
    def __alterar_idade(self):
        self.idade = Input(window=self.menu,
                           size=self.buttons_size,
                           coordinates=self.inputs_coordinate,
                           title="idade",
                           color=self.inputs_color,
                           color_title=self.inputs_color_title)
        self.ajuste_coordenada(self.but_email.coordinates,self.but_email.size,self.space,self.idade)
        self.idade.pack()
        self.alterando = self.idade
        self.idade = int(self.coletar())
        print(self.idade)
        
        
    def __alterar_email(self):    
        self.email = Input(window=self.menu,
                           size=[800,50],
                           coordinates=self.inputs_coordinate,
                           title="email",
                           color=self.inputs_color,
                           color_title=self.inputs_color_title)
        self.ajuste_coordenada(self.but_email.coordinates,self.but_email.size,self.space,self.email)
        self.email.pack()
        self.alterando = self.email
        self.email = self.coletar()
    
    def sair(self):
        self.cancelar = True
        self.loops = False


    def loop(self):
        self.loops = True
        while self.loops:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if events.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for run in self.buts:
                        run.run(pos)
            pygame.display.flip()
                
    def atualizar(self,
                  cnn,
                  nome:str = None,
                  idade:int = None,
                  email:str = None
                  ):
        
        
        try:
            if nome:
                nome= self.tratar_entrada(nome)
            
            user.atualizar_user(conn=cnn,
                                            user_id=self.user_id,
                                            nome=nome,
                                            idade=idade,
                                            email=email)
                
                
            
        except Exception as e:
            print(f"Erro inesperado durante a inclusão: {e}")
            
            self.erro = aviso.Avisos(size_button=self.buttons_size,
                                                coordinates_button=[400,200],
                                                title_button="Erro durante alteração",
                                                color_button="black",
                                                color_title="yellow")
            self.erro.mensagem(f"Erro durante a alteração: {str(e)}")
        # finally:
        #     app = usuario.UsuarioTela()
        #     app.run()
        self.user()

    def coletar(self):
        self.loops = True
        while self.loops:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if events.type == pygame.MOUSEBUTTONDOWN:
                    posinp = pygame.mouse.get_pos()
                    self.retornar = self.alterando.run(pos=posinp)
                    print(self.retornar)
                    self.loops = False
            pygame.display.flip()
        return self.retornar
            
    def confirmar(self):
        self.mid_confirmation = tools.get_obj_center(self.window_size,self.buttons_size)
        self.confirmation = aviso.Avisos(size_button=self.buttons_size,
                                         coordinates_button=[self.mid_confirmation[0],self.space],
                                         title_button="CONFIRMAR",
                                         color_button="black",
                                         color_title="yellow")
        self.verify = self.confirmation.create_confirmation_buttons()

    def tratar_entrada(self, entrada):
        try:
            tratado = re.sub(r'[^a-zA-Z\s]', '', entrada)
            return tratado
        except Exception as e:
            print(f"Erro ao tratar entrada: {e}")
            raise  # Relevanta a exceção após o log para que ela possa ser capturada na chamada
    @staticmethod
    def ajuste_coordenada(coordenada_principal:list[int],
                          tamanho_principal:list[int],
                          espaço:int,
                          inpute:Input):
        coordenada_ajuste_y = coordenada_principal[1]+tamanho_principal[1]+espaço
        new_coordenada_x = tools.get_obj_center([1000,600],inpute.size)
        new_coordenada = [new_coordenada_x[0], coordenada_ajuste_y]
        inpute.coordinates = new_coordenada
    
    def sair_atendimento(self):
        from atendimento import AtendimentoTela
        self.app = AtendimentoTela()
        self.app.run()