from time import sleep
import pygame 
import numpy as np
from sys import exit
from os import system
from os.path import exists
from os import environ
from random import randint

class Serpiente:
    
    def __init__(self): 
        try:
            system("cls")

        except:
            pass

        environ["SDL_VIDEO_CENTERED"] = "1"
        self.iniciar_pantalla()
    
    def iniciar_pantalla(self):
        self.speed = 15
        self.cuerpo = []
        self.newcabeza = ()
        self.newcuerpo = []
        ancho, alto = 600, 600
        self.nanchoC, self.naltoC  = 25, 25
        salida = round(self.naltoC/2) - 1
        self.cabeza = (salida, 1) #y, x
        self.ancho_celda = ancho / self.nanchoC
        self.alto_celda = alto / self.naltoC
        self.gameState = np.zeros((self.naltoC, self.nanchoC), dtype = int)
        self.gameState[self.cabeza] = 1        
        self.newgameState = np.copy(self.gameState)
        self.color_serpiente_cuerpo = (28, 255, 104) 
        self.color_serpiente_cabeza = (10, 179, 66)
        self.color_fondo = (141, 166, 179)
        self.color_manzana_rojo = (255, 28, 50)
        self.letras = (255, 255, 255)
        self.Game = True
        self.Pausa = False
        self.Start = True
        self.move = 3
        self.newmove = 0
        self.puntos = 0
        self.comer = 0
        self.diccionario =  { 
            1: 'arriba',
            2 : 'abajo',
            3 : 'derecha',
            4 : 'izquierda'
            }
        pygame.init()
        pygame.display.set_caption("Snake - Fernando Giráldez Curquejo")
        iconPath = "./icono.ico"

        if exists(iconPath):
            icono = pygame.image.load(iconPath)
            pygame.display.set_icon(icono)

        self.screen = pygame.display.set_mode((ancho, alto))
        self.font = pygame.font.SysFont('Times New Roman', 40)
        self.screen.fill(self.color_fondo)
        text = self.font.render("Score: ", True, self.letras)
        self.screen.blit(text, [0, 0])
        self.clock = pygame.time.Clock()
        self.generar_manzana()
        self.nada_negro()
        self.bucle()

    def generar_manzana(self):
        valores_zero = np.where(self.gameState == 0)
        if len(valores_zero[0]) == 0:
            indice = randint(0 ,len(valores_zero[0]))
        else:
            indice = randint(0 ,(len(valores_zero[0])-1))
        posicion = (valores_zero[0][indice], valores_zero[1][indice])
        self.manzana = posicion

    def nada_negro(self):
        self.screen.fill(self.color_fondo)
        for y in range(self.naltoC):
            for x in range(self.nanchoC):
                cordenada = (y, x)                 
                poly = (x * self.ancho_celda, y * self.alto_celda, self.ancho_celda, self.alto_celda)
                
                if cordenada == self.manzana:
                    pygame.draw.rect(self.screen, self.color_manzana_rojo, poly) 
                
                elif cordenada == self.cabeza:
                    pygame.draw.rect(self.screen, self.color_serpiente_cabeza, poly)

                elif cordenada in self.cuerpo:
                    pygame.draw.rect(self.screen, self.color_serpiente_cuerpo, poly)

        text = self.font.render("Score: " + str(self.puntos), True, self.letras)
        self.screen.blit(text, [0, 0])
        pygame.display.update() 

    def movimiento_colision(self):
        if self.newcabeza in self.newcuerpo:
            self.Game = False

        x, y = self.newcabeza 
        
        if x > (self.naltoC-1) or x < 0:
            self.Game = False

        if y > (self.nanchoC-1) or y < 0:
            self.Game = False

        if self.newcabeza == self.manzana:
            if len(self.cuerpo) >= 1: 
                self.newcuerpo.append(self.cuerpo[-1])
            else:
                self.newcuerpo.append(self.cabeza)
            self.puntos += 1
            self.comer = 1

        self.cabeza = self.newcabeza
        self.cuerpo = self.newcuerpo
        self.newcabeza = ()
        self.newcuerpo = []
        self.screen.fill(self.color_fondo)

        if self.Game:
            self.newgameState[self.cabeza] = 1
            
            for cordenada in self.cuerpo:
                self.newgameState[cordenada] = 1

            self.gameState = np.copy(self.newgameState)

            if self.comer == 1:
                self.generar_manzana()
                self.comer = 0  
        
            self.newgameState = np.zeros((self.naltoC, self.nanchoC), dtype=int)
        
    def mover_cuerpo(self):
        if len(self.cuerpo) >= 1:
            for numero in range(len(self.cuerpo)):
                if numero == 0:
                    self.newcuerpo.append(self.cabeza)
                else:
                    self.newcuerpo.append(self.cuerpo[(numero-1)])

    def arriba(self):
        y, x = self.cabeza  
        y -= 1
        self.newcabeza = (y, x)
        self.mover_cuerpo()   
        self.movimiento_colision() 
    
    def abajo(self):
        y, x = self.cabeza  
        y += 1
        self.newcabeza = (y, x)
        self.mover_cuerpo()   
        self.movimiento_colision() 
    
    def derecha(self):
        y, x= self.cabeza  
        x += 1
        self.newcabeza = (y, x)
        self.mover_cuerpo()   
        self.movimiento_colision() 
 
    def izquierda(self):
        y, x = self.cabeza  
        x -= 1
        self.newcabeza = (y, x)
        self.mover_cuerpo()   
        self.movimiento_colision() 

    def moverse_actualizar(self):
        if self.newmove == 1:
            self.move = 1

        elif self.newmove == 2:
            self.move = 2

        elif self.newmove == 3:
            self.move = 3

        elif self.newmove == 4:
            self.move = 4

    def comprobar_moverse(self):
        if len(self.cuerpo) >= 1:
            if self.newmove == 1 and self.move == 2:
                self.newmove = 2 
            
            elif self.newmove == 2 and self.move == 1:
                self.newmove = 1
            
            elif self.newmove == 3 and self.move == 4:
                self.newmove = 4
            
            elif self.newmove == 4 and self.move == 3:
                self.newmove = 3 
            
            self.moverse_actualizar()
            self.moverse()
        
        else:
            self.moverse_actualizar()  
            self.moverse()
            
    def moverse(self):
        if self.move == 1:
            self.arriba()
        elif self.move == 2:
            self.abajo()
        elif self.move == 3:
            self.derecha()
        elif self.move == 4:
            self.izquierda()

    def bucle(self):
        while self.Game:
            ev = pygame.event.get()
            for event in ev:
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.Game = False
                    exit()

                if event.type == pygame.KEYDOWN:
                    
                    if not self.Pausa:
                        if event.key == pygame.K_UP:
                            self.newmove = 1
                        
                        if event.key == pygame.K_DOWN:
                            self.newmove = 2
                            
                        if event.key == pygame.K_RIGHT:
                            self.newmove = 3

                        if event.key == pygame.K_LEFT:
                            self.newmove = 4

                    if event.key == pygame.K_p:
                        self.Pausa = not self.Pausa

                    if event.key == pygame.K_SPACE:
                        self.Pausa = not self.Pausa

                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        self.Game = False
                        exit()

                    if self.Start:
                        self.Start = False
                        self.newmove = 3
            
            if not self.Start:
        
                if not self.Pausa:
                    
                    self.comprobar_moverse()
                    self.screen.fill(self.color_fondo)
                    
                    #Dibujar Manzana
                    y, x = self.manzana        
                    poly = (x * self.ancho_celda, y * self.alto_celda, self.ancho_celda, self.alto_celda)
                    pygame.draw.rect(self.screen, self.color_manzana_rojo, poly) 

                    #Dibujar cabeza
                    y, x = self.cabeza        
                    poly = (x * self.ancho_celda, y * self.alto_celda, self.ancho_celda, self.alto_celda)
                    pygame.draw.rect(self.screen, self.color_serpiente_cabeza, poly)

                    #Dibujar cuerpo
                    for cordenada in self.cuerpo:
                        y, x = cordenada       
                        poly = (x * self.ancho_celda, y * self.alto_celda, self.ancho_celda, self.alto_celda)
                        pygame.draw.rect(self.screen, self.color_serpiente_cuerpo, poly)

                    text = self.font.render("Score: " + str(self.puntos), True, self.letras)
                    self.screen.blit(text, [0, 0])
                    text = self.font.render("Score: " + str(self.puntos), True, self.letras)
                    self.screen.blit(text, [0, 0])
                    pygame.display.update()
                    self.clock.tick(self.speed)
                
                else:
                    self.screen.fill(self.color_fondo)
                    text = self.font.render("Pausa", True, self.letras)
                    self.screen.blit(text, [0, 0])
                    text = self.font.render("Presione p o espacio para continuar", True, self.letras)
                    self.screen.blit(text, [0, 50])
                    text = self.font.render("Presione escape para salir", True, self.letras)
                    self.screen.blit(text, [0, 100])
                    pygame.display.update()

                if self.puntos == (self.naltoC*self.nanchoC-2):
                    self.screen.fill(self.color_fondo)
                    text = self.font.render('Has Ganado', True, self.color_manzana_rojo)
                    self.screen.blit(text, [0, 0])
                    pygame.display.update()
                    sleep(5)
                    pygame.quit()
                    exit()

                if self.Game == False:
                    self.screen.fill(self.color_fondo)
                    text = self.font.render("Score: " + str(self.puntos), True, self.color_manzana_rojo)
                    self.screen.blit(text, [0, 0])
                    text = self.font.render("Fin del juego", True, self.letras)
                    self.screen.blit(text, [0, 50])
                    pygame.display.update()
                    sleep(5)
                    pygame.quit()
                    exit()

if __name__ == "__main__":
    snake = Serpiente()