import pygame
import random
import config


class Ground:
    ground_level = 450  # Ajustado para dar espacio a la imagen del suelo

    def __init__(self, win_width):
        self.x, self.y = 0, Ground.ground_level
        self.width = win_width
        self.rect = pygame.Rect(self.x, self.y, win_width, 50)
        # Para mover el suelo
        self.x1 = 0
        self.x2 = self.width

    def draw(self, window):
        # Si estamos en modo juego y las imágenes están cargadas
        if config.game_mode == 'play' and config.BASE_IMG:
            # Dibujar dos imágenes de base para crear efecto de movimiento continuo
            window.blit(config.BASE_IMG, (self.x1, self.y))
            window.blit(config.BASE_IMG, (self.x2, self.y))
            
            # Mover las bases
            self.x1 -= 1
            self.x2 -= 1
            
            # Reposicionar las bases cuando salen de la pantalla
            if self.x1 + self.width < 0:
                self.x1 = self.x2 + self.width
            if self.x2 + self.width < 0:
                self.x2 = self.x1 + self.width
        else:
            # Dibujar el suelo original (solo una línea)
            pygame.draw.rect(window, (255, 255, 255), self.rect)


class Pipes:
    width = 52  # Ancho ajustado para la imagen
    opening = 150  # Apertura entre tuberías aumentada para gráficos

    def __init__(self, win_width):
        self.x = win_width
        self.bottom_height = random.randint(50, 250)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening
        self.bottom_rect = pygame.Rect(self.x, Ground.ground_level - self.bottom_height, self.width, self.bottom_height)
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.passed = False
        self.off_screen = False

    def draw(self, window):
        # Actualizar rectángulos para colisiones
        self.bottom_rect = pygame.Rect(self.x, Ground.ground_level - self.bottom_height, self.width, self.bottom_height)
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        
        if config.game_mode == 'play' and config.PIPE_IMG:
            # Dibujar pipe inferior
            window.blit(config.PIPE_IMG, (self.x, Ground.ground_level - self.bottom_height))
            
            # Dibujar pipe superior (girada)
            top_pipe = pygame.transform.flip(config.PIPE_IMG, False, True)
            window.blit(top_pipe, (self.x, self.top_height - 320))
        else:
            # Dibujar rectángulos simples en modo entrenamiento
            pygame.draw.rect(window, (255, 255, 255), self.bottom_rect)
            pygame.draw.rect(window, (255, 255, 255), self.top_rect)

    def update(self):
        self.x -= 1
        if self.x + Pipes.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True