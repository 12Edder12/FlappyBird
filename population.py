import pygame
import config
import player
import math
import species
import operator
import os
import csv


class Population:
    """
    La clase Population gestiona un conjunto de jugadores y coordina el proceso evolutivo.
    Implementa la selección natural, especiación y generación de nuevas poblaciones.
    """
    
    def __init__(self, size):
        """
        Inicializa una población de jugadores (pájaros).
        
        Args:
            size: Número de jugadores en la población
        """
        self.players = []                # Lista de jugadores
        self.generation = 1              # Contador de generaciones
        self.species = []                # Lista de especies
        self.size = size                 # Tamaño de la población
        self.best_player = None          # Mejor jugador encontrado
        self.best_fitness = 0            # Mayor fitness encontrado
        self.iterations_limit = 0        # Límite de generaciones (0 = sin límite)
        
        # Crear la población inicial con jugadores aleatorios
        for i in range(0, self.size):
            self.players.append(player.Player())

    def update_live_players(self):
        """
        Actualiza todos los jugadores vivos en la población.
        Cada jugador observa el entorno, piensa, se dibuja y actualiza su posición.
        También actualiza el registro del mejor jugador si es necesario.
        """
        for p in self.players:
            if p.alive:
                p.look()                 # El jugador observa el entorno
                p.think()                # El jugador decide si aletear
                p.draw(config.window)    # Se dibuja el jugador en la ventana
                p.update(config.ground)  # Se actualiza su posición
                
                # Actualizar el registro del mejor jugador si este ha sobrevivido más tiempo
                if p.lifespan > self.best_fitness:
                    self.best_fitness = p.lifespan
                    self.best_player = p

    def natural_selection(self):
        """
        Realiza el proceso de selección natural al finalizar una generación.
        Agrupa a los jugadores en especies, calcula su fitness, elimina especies no productivas,
        y genera la siguiente generación de jugadores.
        """
        print(f'Generación {self.generation} completada. Mejor fitness: {self.best_fitness}')
        
        # Verificar si se alcanzó el límite de generaciones
        if self.iterations_limit is not None and self.iterations_limit > 0 and self.generation >= self.iterations_limit:
            print(f"¡Límite de {self.iterations_limit} generaciones alcanzado!")
            self.save_best_player()      # Guardar el mejor jugador
            pygame.quit()                # Cerrar el juego
            return
        
        self.speciate()                  # Agrupar jugadores en especies
        self.calculate_fitness()         # Calcular fitness de jugadores y especies
        self.kill_extinct_species()      # Eliminar especies sin jugadores
        self.kill_stale_species()        # Eliminar especies estancadas
        self.sort_species_by_fitness()   # Ordenar especies por fitness
        self.next_gen()                  # Generar la siguiente generación

    def speciate(self):
        """
        Agrupa a los jugadores en especies basándose en la similitud entre sus cerebros.
        Si un jugador es similar a una especie existente, se añade a ella.
        En caso contrario, se crea una nueva especie para ese jugador.
        """
        # Limpiar jugadores de todas las especies
        for s in self.species:
            s.players = []

        # Asignar cada jugador a una especie
        for p in self.players:
            add_to_species = False
            # Buscar una especie compatible para el jugador
            for s in self.species:
                if s.similarity(p.brain):
                    s.add_to_species(p)  # Añadir a la especie existente
                    add_to_species = True
                    break
            # Si no hay especie compatible, crear una nueva
            if not add_to_species:
                self.species.append(species.Species(p))

    def calculate_fitness(self):
        """
        Calcula el fitness de cada jugador y actualiza el registro del mejor jugador.
        También calcula el fitness promedio de cada especie.
        """
        # Calcular fitness individual de cada jugador
        for p in self.players:
            p.calculate_fitness()
            # Actualizar mejor jugador global si es necesario
            if p.fitness > self.best_fitness:
                self.best_fitness = p.fitness
                self.best_player = p
        
        # Calcular fitness promedio de cada especie
        for s in self.species:
            s.calculate_average_fitness()

    def kill_extinct_species(self):
        """
        Elimina especies que no tienen jugadores (extintas).
        """
        species_bin = []
        # Identificar especies sin jugadores
        for s in self.species:
            if len(s.players) == 0:
                species_bin.append(s)
        # Eliminar las especies identificadas
        for s in species_bin:
            self.species.remove(s)

    def kill_stale_species(self):
        """
        Elimina especies que no han mejorado en varias generaciones (estancadas).
        Si la especie tiene una "staleness" (estancamiento) >= 8, se elimina.
        Se conserva al menos una especie, incluso si todas están estancadas.
        """
        player_bin = []   # Jugadores a eliminar
        species_bin = []  # Especies a eliminar
        
        for s in self.species:
            if s.staleness >= 8:  # Si la especie no ha mejorado en 8 generaciones
                # Solo eliminar si quedaría al menos una especie
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(s)
                    # Marcar todos los jugadores de la especie para eliminar
                    for p in s.players:
                        player_bin.append(p)
                else:
                    # Resetear el estancamiento de la última especie
                    s.staleness = 0
        
        # Eliminar los jugadores y especies marcados
        for p in player_bin:
            self.players.remove(p)
        for s in species_bin:
            self.species.remove(s)

    def sort_species_by_fitness(self):
        """
        Ordena los jugadores dentro de cada especie por fitness.
        Luego ordena las especies por su fitness de referencia (benchmark_fitness).
        """
        # Ordenar jugadores dentro de cada especie
        for s in self.species:
            s.sort_players_by_fitness()

        # Ordenar especies de mayor a menor fitness
        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def next_gen(self):
        """
        Crea la siguiente generación de jugadores.
        Incluye el campeón de cada especie y genera descendencia proporcional al fitness.
        """
        children = []  # Lista para la nueva generación

        # Añadir un clon del campeón de cada especie (elitismo)
        for s in self.species:
            children.append(s.champion.clone())

        # Distribuir el resto de slots entre las especies según su fitness
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for s in self.species:
            # Generar descendencia para cada especie
            for i in range(0, children_per_species):
                children.append(s.offspring())

        # Si aún faltan jugadores, llenarlos con descendencia de la mejor especie
        while len(children) < self.size:
            children.append(self.species[0].offspring())

        # Reemplazar la población anterior con los nuevos jugadores
        self.players = []
        for child in children:
            self.players.append(child)
        
        # Incrementar el contador de generaciones
        self.generation += 1

    def extinct(self):
        """
        Verifica si todos los jugadores han muerto (están extintos).
        
        Returns:
            True si todos los jugadores están muertos, False en caso contrario.
        """
        extinct = True
        for p in self.players:
            if p.alive:
                extinct = False
        return extinct
        
    def save_best_player(self):
        """
        Guarda el mejor jugador encontrado como un archivo CSV.
        También guarda un archivo de información con detalles sobre el modelo.
        """
        if self.best_player:
            # Crear directorio models si no existe
            if not os.path.exists('models'):
                os.makedirs('models')
            
            # Encontrar el siguiente número modelo disponible
            model_num = 1
            while os.path.exists(f'models/modelo{model_num}.csv'):
                model_num += 1
            
            filename = f'models/modelo{model_num}.csv'
            
            # Guardar los pesos en un archivo CSV
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                for conn in self.best_player.brain.connections:
                    writer.writerow([conn.weight])
            
            print(f"Modelo guardado como: {filename}")
            print(f"Generaciones: {self.generation}, Fitness: {self.best_fitness}")
            
            # Guardar información del modelo en un archivo de texto
            with open(f'models/modelo{model_num}_info.txt', 'w') as f:
                f.write(f"Generaciones: {self.generation}\n")
                f.write(f"Fitness: {self.best_fitness}\n")
                f.write(f"Fecha de creacion: {import_datetime().now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Poblacion: {self.size}\n")
                f.write(f"Iteraciones: {self.iterations_limit}\n")
        else:
            print("No hay jugador para guardar")

# Función auxiliar para importar datetime solo cuando es necesario
def import_datetime():
    """
    Importa el módulo datetime solo cuando es necesario.
    Esto evita importarlo al inicio del archivo si no se usa.
    """
    import datetime
    return datetime.datetime