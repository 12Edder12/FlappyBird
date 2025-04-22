import pygame

# Window settings
win_width = 400
win_height = 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("FlappyBird AI")

# Game objects
pipes = []

# Game resources
ground = None

# Assets
BIRD_IMGS = []
PIPE_IMG = None
BASE_IMG = None
BG_IMG = None

# Global variables
game_mode = None  # 'train' or 'play'
selected_model = None

# Función para cargar imágenes
def load_images():
    global BIRD_IMGS, PIPE_IMG, BASE_IMG, BG_IMG
    
    # Cargar imágenes del pájaro
    BIRD_IMGS = [
        pygame.transform.scale(pygame.image.load('assets/bird1.png'), (34, 24)),
        pygame.transform.scale(pygame.image.load('assets/bird2.png'), (34, 24)),
        pygame.transform.scale(pygame.image.load('assets/bird3.png'), (34, 24))
    ]
    
    # Cargar imagen de la tubería y girarla para la parte superior
    PIPE_IMG = pygame.transform.scale(pygame.image.load('assets/pipe.png'), (52, 320))
    
    # Cargar imagen del suelo y fondo
    BASE_IMG = pygame.transform.scale(pygame.image.load('assets/base.png'), (win_width, 70))
    BG_IMG = pygame.transform.scale(pygame.image.load('assets/bg.png'), (win_width, win_height))