import brain
import random
import pygame
import config
import math


class Player:
    def __init__(self):
    # Bird
        self.x, self.y = 50, 200  # Posición inicial del pájaro
        self.rect = pygame.Rect(self.x, self.y, 34, 24)  # Rectángulo de colisión
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)  # Color aleatorio
        self.vel = 0  # Velocidad vertical inicial
        self.flap = False  # Estado del aleteo
        self.alive = True  # Estado de vida
        self.lifespan = 0  # Contador de tiempo de vida (frames)
        
        # Animación
        self.img_count = 0  # Contador para la animación
        self.img_index = 0  # Índice de la imagen actual
        self.tilt = 0  # Inclinación del pájaro

        # AI
        self.decision = None  # Resultado de la decisión de la IA
        self.vision = [0.5, 1, 0.5]  # Datos de entrada para la IA (visión)
        self.fitness = 0  # Puntuación de aptitud para el algoritmo genético
        self.inputs = 3  # Número de entradas para la red neuronal
        self.brain = brain.Brain(self.inputs)  # Crea una red neuronal
        self.brain.generate_net()  # Inicializa la red neuronal

    # Game related functions
    def draw(self, window):
        if config.game_mode == 'play' and config.BIRD_IMGS:
            # Gestionar animación del pájaro
            self.img_count += 1
            
            # Determinar qué imagen mostrar basado en img_count
            if self.img_count < 5:
                self.img_index = 0
            elif self.img_count < 10:
                self.img_index = 1
            elif self.img_count < 15:
                self.img_index = 2
            elif self.img_count < 20:
                self.img_index = 1
            elif self.img_count == 20:
                self.img_index = 0
                self.img_count = 0
                
            # Rotar el pájaro según la velocidad
            if self.vel < 0:
                self.tilt = 25  # Hacia arriba cuando sube
            elif self.vel > 2.5:
                self.tilt = -90  # Hacia abajo cuando cae rápido
                self.img_index = 1  # Usar imagen central durante la caída
            
            # Rotar y dibujar la imagen del pájaro
            rotated_image = pygame.transform.rotate(config.BIRD_IMGS[self.img_index], self.tilt)
            rect = rotated_image.get_rect(center=self.rect.center)
            window.blit(rotated_image, rect.topleft)
        else:
            # Modo entrenamiento: dibujar rectángulo simple
            pygame.draw.rect(window, self.color, self.rect)

    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)

    def sky_collision(self):
        return bool(self.rect.y < 10)

    def pipe_collision(self):
        for p in config.pipes:
            return pygame.Rect.colliderect(self.rect, p.top_rect) or \
                   pygame.Rect.colliderect(self.rect, p.bottom_rect)

    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision() or self.sky_collision()):
            # Gravity
            self.vel += 0.3
            self.rect.y += self.vel
            if self.vel > 6:
                self.vel = 6
            # Increment lifespan
            self.lifespan += 1
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -6  # Ajustado para un salto más natural
        if self.vel >= 3:
            self.flap = False

    @staticmethod
    def closest_pipe():
        for p in config.pipes:
            if not p.passed:
                return p
        return None  # En caso de que no haya tubos

    # AI related functions
    def look(self):
        closest = self.closest_pipe()
        if config.pipes and closest:
            # Line to top pipe
            self.vision[0] = max(0, self.rect.center[1] - closest.top_rect.bottom) / 500
            if config.game_mode != 'play':  # Solo mostrar líneas en modo entrenamiento
                pygame.draw.line(config.window, self.color, self.rect.center,
                                (self.rect.center[0], closest.top_rect.bottom))

            # Line to mid pipe
            self.vision[1] = max(0, closest.x - self.rect.center[0]) / 500
            if config.game_mode != 'play':
                pygame.draw.line(config.window, self.color, self.rect.center,
                                (closest.x, self.rect.center[1]))

            # Line to bottom pipe
            self.vision[2] = max(0, closest.bottom_rect.top - self.rect.center[1]) / 500
            if config.game_mode != 'play':
                pygame.draw.line(config.window, self.color, self.rect.center,
                                (self.rect.center[0], closest.bottom_rect.top))

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone

    # Cargar los pesos desde un archivo CSV
    def load_weights_from_csv(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                if len(lines) != len(self.brain.connections):
                    print(f"Error: El modelo tiene {len(lines)} conexiones pero se esperaban {len(self.brain.connections)}")
                    return False
                
                for i, line in enumerate(lines):
                    weight = float(line.strip())
                    self.brain.connections[i].weight = weight
                
                self.brain.generate_net()
                return True
        except Exception as e:
            print(f"Error al cargar el modelo: {str(e)}")
            return False