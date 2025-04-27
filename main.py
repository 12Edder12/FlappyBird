import pygame
from sys import exit
import config
import components
import population
import player
import os
import time
import re

# Inicializar pygame
pygame.init()
clock = pygame.time.Clock()

# Inicializar configuración
config.win_width = 400
config.win_height = 500
config.window = pygame.display.set_mode((config.win_width, config.win_height))
pygame.display.set_caption("FlappyBird AI")

# Inicializar pipes como lista vacía
config.pipes = []

def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        return event
    return None

def load_assets():
    try:
        # Crear directorio assets si no existe
        if not os.path.exists('assets'):
            os.makedirs('assets')
            print("El directorio 'assets' ha sido creado. Por favor, coloca las imágenes necesarias.")
            print("El juego funcionará sin gráficos hasta que las imágenes estén disponibles.")
        else:
            # Intentar cargar las imágenes
            config.load_images()
            print("Imágenes cargadas correctamente.")
    except Exception as e:
        print(f"Error al cargar imágenes: {str(e)}")
        print("El juego funcionará con gráficos simples.")

def draw_background():
    """Dibuja el fondo en la ventana del juego"""
    try:
        # Intentar cargar directamente la imagen de fondo
        if not hasattr(config, 'BG_IMG') or config.BG_IMG is None:
            if os.path.exists('assets/background.png'):
                config.BG_IMG = pygame.image.load('assets/background.png')
                # Ajustar tamaño si es necesario
                config.BG_IMG = pygame.transform.scale(config.BG_IMG, (config.win_width, config.win_height))
        
        # Dibujar la imagen si existe
        if hasattr(config, 'BG_IMG') and config.BG_IMG:
            config.window.blit(config.BG_IMG, (0, 0))
        else:
            config.window.fill((0, 0, 0))
    except Exception as e:
        print(f"Error cargando fondo: {str(e)}")
        config.window.fill((0, 0, 0))

def show_menu():
    # Dibujar fondo
    draw_background()
    
    font = pygame.font.SysFont('Arial', 32)
    title = font.render('FlappyBird AI', True, (255, 255, 255))
    option1 = font.render('1. Entrenamiento', True, (255, 255, 255))
    option2 = font.render('2. Jugar', True, (255, 255, 255))
    exit_text = font.render('0. Salir', True, (255, 255, 255))
    
    # Añadir un fondo semi-transparente a los textos para mejorar legibilidad
    title_bg = pygame.Surface((title.get_width() + 20, title.get_height() + 10), pygame.SRCALPHA)
    title_bg.fill((0, 0, 0, 150))
    option1_bg = pygame.Surface((option1.get_width() + 20, option1.get_height() + 10), pygame.SRCALPHA)
    option1_bg.fill((0, 0, 0, 150))
    option2_bg = pygame.Surface((option2.get_width() + 20, option2.get_height() + 10), pygame.SRCALPHA)
    option2_bg.fill((0, 0, 0, 150))
    exit_bg = pygame.Surface((exit_text.get_width() + 20, exit_text.get_height() + 10), pygame.SRCALPHA)
    exit_bg.fill((0, 0, 0, 150))
    
    # Dibujar fondos y textos
    config.window.blit(title_bg, (config.win_width//2 - (title.get_width() + 20)//2, 45))
    config.window.blit(title, (config.win_width//2 - title.get_width()//2, 50))
    
    config.window.blit(option1_bg, (40, 145))
    config.window.blit(option1, (50, 150))
    
    config.window.blit(option2_bg, (40, 195))
    config.window.blit(option2, (50, 200))
    
    config.window.blit(exit_bg, (40, 245))
    config.window.blit(exit_text, (50, 250))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    waiting = False
                    return 'train'
                elif event.key == pygame.K_2:
                    waiting = False
                    return 'play'
                elif event.key == pygame.K_0:
                    pygame.quit()
                    exit()
        clock.tick(15)

def get_saved_models():
    models = []
    if os.path.exists('models'):
        for file in os.listdir('models'):
            if file.endswith('.csv') and file.startswith('modelo'):
                try:
                    # Extraer número del modelo con regex
                    match = re.search(r'modelo(\d+)\.csv', file)
                    if match:
                        model_num = int(match.group(1))
                        models.append((model_num, file))
                except:
                    pass
    
    # Ordenar modelos por número
    models.sort()
    return models

def show_models_list():
    models = get_saved_models()
    
    # Dibujar fondo
    draw_background()
    
    if not models:
        font = pygame.font.SysFont('Arial', 24)
        title = font.render('No hay modelos guardados', True, (255, 255, 255))
        back = font.render('Presione cualquier tecla para volver', True, (255, 255, 255))
        
        # Añadir fondos semi-transparentes
        title_bg = pygame.Surface((title.get_width() + 20, title.get_height() + 10), pygame.SRCALPHA)
        title_bg.fill((0, 0, 0, 150))
        back_bg = pygame.Surface((back.get_width() + 20, back.get_height() + 10), pygame.SRCALPHA)
        back_bg.fill((0, 0, 0, 150))
        
        config.window.blit(title_bg, (config.win_width//2 - (title.get_width() + 20)//2, 145))
        config.window.blit(title, (config.win_width//2 - title.get_width()//2, 150))
        
        config.window.blit(back_bg, (config.win_width//2 - (back.get_width() + 20)//2, 195))
        config.window.blit(back, (config.win_width//2 - back.get_width()//2, 200))
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    return None
            clock.tick(15)
    
    font = pygame.font.SysFont('Arial', 24)
    title = font.render('Seleccione un modelo:', True, (255, 255, 255))
    
    # Fondo semi-transparente para el título
    title_bg = pygame.Surface((title.get_width() + 20, title.get_height() + 10), pygame.SRCALPHA)
    title_bg.fill((0, 0, 0, 150))
    config.window.blit(title_bg, (config.win_width//2 - (title.get_width() + 20)//2, 45))
    config.window.blit(title, (config.win_width//2 - title.get_width()//2, 50))
    
    # Panel semi-transparente para la lista de modelos
    list_height = len(models) * 40 + 50  # Altura para los modelos + botón volver
    list_bg = pygame.Surface((350, list_height), pygame.SRCALPHA)
    list_bg.fill((0, 0, 0, 150))
    config.window.blit(list_bg, (25, 95))
    
    for i, (model_num, filename) in enumerate(models):
        # Obtener info del modelo si existe
        info_text = ""
        info_file = f'models/modelo{model_num}_info.txt'
        if os.path.exists(info_file):
            try:
                with open(info_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        info_text = f" - Gen: {lines[0].split(':')[1].strip()}, Fitness: {lines[1].split(':')[1].strip()}"
            except:
                pass
        
        option = font.render(f"{i+1}. {filename}{info_text}", True, (255, 255, 255))
        config.window.blit(option, (30, 100 + i * 40))
    
    back = font.render('0. Volver', True, (255, 255, 255))
    config.window.blit(back, (30, 100 + len(models) * 40))
    
    pygame.display.flip()
    
    waiting = True
    selection = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    waiting = False
                    return None
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    idx = event.key - pygame.K_1
                    if idx < len(models):
                        waiting = False
                        selection = models[idx][1]
        clock.tick(15)
    
    return selection

def play_with_model(model_path):
    # Configurar el modo de juego
    config.game_mode = 'play'
    
    # Crear el jugador y cargar el modelo
    p = player.Player()
    if not p.load_weights_from_csv(f'models/{model_path}'):
        return
    
    # Configuración del juego
    pipes_spawn_time = 10
    config.ground = components.Ground(config.win_width)
    
    # Bucle principal del juego
    running = True
    while running:
        event = quit_game()
        if event and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            
        # Dibujar fondo
        draw_background()
        
        # Información del modelo - con fondo semi-transparente
        font = pygame.font.SysFont('Arial', 16)
        info_text = font.render(f"Modelo: {model_path}", True, (255, 255, 255))
        score_text = font.render(f"Puntuación: {p.lifespan}", True, (255, 255, 255))
        
        info_bg = pygame.Surface((max(info_text.get_width(), score_text.get_width()) + 20, 50), pygame.SRCALPHA)
        info_bg.fill((0, 0, 0, 150))
        config.window.blit(info_bg, (5, 5))
        
        config.window.blit(info_text, (10, 10))
        config.window.blit(score_text, (10, 30))
        
        # Generar tuberías
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1
        
        # Actualizar y dibujar tuberías
        to_remove = []
        for pipe in config.pipes:
            pipe.update()
            if pipe.off_screen:
                to_remove.append(pipe)
        
        for pipe in to_remove:
            if pipe in config.pipes:
                config.pipes.remove(pipe)
        
        # Actualizar y dibujar jugador
        if p.alive:
            p.look()
            p.think()
            p.update(config.ground.rect)
            
        else:
            # Juego terminado
            game_over = font.render("¡Game Over! Presiona ESC para volver", True, (255, 255, 255))
            game_over_bg = pygame.Surface((game_over.get_width() + 20, game_over.get_height() + 10), pygame.SRCALPHA)
            game_over_bg.fill((0, 0, 0, 150))
            config.window.blit(game_over_bg, (config.win_width//2 - (game_over.get_width() + 20)//2, config.win_height//2 - 5))
            config.window.blit(game_over, (config.win_width//2 - game_over.get_width()//2, config.win_height//2))
        
        # Dibujar tuberías después de actualizar
        for pipe in config.pipes:
            pipe.draw(config.window)
            
        # Dibujar el suelo después de todo
        config.ground.draw(config.window)
        
        # Dibujar el jugador por encima del suelo
        if p.alive:
            p.draw(config.window)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Limpiar para volver al menú
    config.pipes.clear()
    config.game_mode = None

def train_population(population_size=1000):
    # Configurar el modo de entrenamiento
    config.game_mode = 'train'
    
    # Inicializar población
    pop = population.Population(population_size)
    # Establecer límite de iteraciones a None para indicar entrenamiento infinito
    pop.iterations_limit = None
    
    # Configuración del juego
    pipes_spawn_time = 10
    config.ground = components.Ground(config.win_width)
    
    # Variables para guardar automáticamente
    last_save_time = time.time()
    auto_save_interval = 300  # Guardar cada 5 minutos
    
    # Bucle principal de entrenamiento
    running = True
    while running:
        event = quit_game()
        if event and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Guardar antes de salir
            pop.save_best_player()
            running = False
            
        # Dibujar fondo
        draw_background()
        
        # Guardar automáticamente cada cierto tiempo
        current_time = time.time()
        if current_time - last_save_time > auto_save_interval:
            pop.save_best_player()
            last_save_time = current_time
        
        # Mostrar información del entrenamiento con fondo semi-transparente
        font = pygame.font.SysFont('Arial', 16)
        gen_text = font.render(f"Generación: {pop.generation} (Infinito)", True, (255, 255, 255))
        alive_text = font.render(f"Vivos: {sum(1 for p in pop.players if p.alive)}/{len(pop.players)}", True, (255, 255, 255))
        fitness_text = font.render(f"Mejor Fitness: {pop.best_fitness}", True, (255, 255, 255))
        time_since_save = current_time - last_save_time
        save_text = font.render(f"Último guardado: hace {int(time_since_save)}s", True, (255, 255, 255))
        esc_text = font.render("ESC para guardar y salir", True, (255, 255, 255))
        
        # Crear un fondo semi-transparente para todos los textos
        max_width = max(gen_text.get_width(), alive_text.get_width(), 
                       fitness_text.get_width(), save_text.get_width(), 
                       esc_text.get_width()) + 20
        info_bg = pygame.Surface((max_width, 110), pygame.SRCALPHA)
        info_bg.fill((0, 0, 0, 150))
        config.window.blit(info_bg, (5, 5))
        
        config.window.blit(gen_text, (10, 10))
        config.window.blit(alive_text, (10, 30))
        config.window.blit(fitness_text, (10, 50))
        config.window.blit(save_text, (10, 70))
        config.window.blit(esc_text, (10, 90))
        
        # Generar tuberías
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1
        
        # Actualizar y dibujar tuberías
        to_remove = []
        for pipe in config.pipes:
            pipe.draw(config.window)
            pipe.update()
            if pipe.off_screen:
                to_remove.append(pipe)
        
        for pipe in to_remove:
            if pipe in config.pipes:
                config.pipes.remove(pipe)
        
        # Dibujar el suelo
        config.ground.draw(config.window)
        
        # Actualizar todos los jugadores vivos
        if not pop.extinct():
            pop.update_live_players()
        else:
            # Cuando todos están muertos, hacer selección natural y reiniciar
            config.pipes.clear()
            pop.natural_selection()
            pipes_spawn_time = 10
        
        pygame.display.flip()
        clock.tick(60)
    
    # Limpiar para volver al menú
    config.pipes.clear()
    config.game_mode = None

def main():
    # Cargar recursos si están disponibles
    load_assets()
    
    # Inicializar el suelo
    config.ground = components.Ground(config.win_width)
    
    # Bucle principal del programa
    running = True
    while running:
        # Mostrar menú principal
        choice = show_menu()
        
        if choice == 'train':
            # Iniciar entrenamiento infinito
            train_population()
        
        elif choice == 'play':
            # Mostrar lista de modelos
            model = show_models_list()
            if model is not None:
                # Jugar con el modelo seleccionado
                play_with_model(model)
        
        else:
            running = False

if __name__ == "__main__":
    main()