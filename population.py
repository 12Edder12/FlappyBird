import pygame
import config
import player
import math
import species
import operator
import os
import csv


class Population:
    def __init__(self, size):
        self.players = []
        self.generation = 1
        self.species = []
        self.size = size
        self.best_player = None
        self.best_fitness = 0
        self.iterations_limit = 0
        
        for i in range(0, self.size):
            self.players.append(player.Player())

    def update_live_players(self):
        for p in self.players:
            if p.alive:
                p.look()
                p.think()
                p.draw(config.window)
                p.update(config.ground)
                
                # Actualizar mejor jugador
                if p.lifespan > self.best_fitness:
                    self.best_fitness = p.lifespan
                    self.best_player = p

    def natural_selection(self):
        print(f'Generación {self.generation} completada. Mejor fitness: {self.best_fitness}')
        
        # Verificar si hemos alcanzado el límite de iteraciones
        if self.iterations_limit is not None and self.iterations_limit > 0 and self.generation >= self.iterations_limit:
            print(f"¡Límite de {self.iterations_limit} generaciones alcanzado!")
            self.save_best_player()
            pygame.quit()
            return
        
        self.speciate()
        self.calculate_fitness()
        self.kill_extinct_species()
        self.kill_stale_species()
        self.sort_species_by_fitness()
        self.next_gen()

    def speciate(self):
        for s in self.species:
            s.players = []

        for p in self.players:
            add_to_species = False
            for s in self.species:
                if s.similarity(p.brain):
                    s.add_to_species(p)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(p))

    def calculate_fitness(self):
        for p in self.players:
            p.calculate_fitness()
            if p.fitness > self.best_fitness:
                self.best_fitness = p.fitness
                self.best_player = p
        for s in self.species:
            s.calculate_average_fitness()

    def kill_extinct_species(self):
        species_bin = []
        for s in self.species:
            if len(s.players) == 0:
                species_bin.append(s)
        for s in species_bin:
            self.species.remove(s)

    def kill_stale_species(self):
        player_bin = []
        species_bin = []
        for s in self.species:
            if s.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(s)
                    for p in s.players:
                        player_bin.append(p)
                else:
                    s.staleness = 0
        for p in player_bin:
            self.players.remove(p)
        for s in species_bin:
            self.species.remove(s)

    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_players_by_fitness()

        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def next_gen(self):
        children = []

        # Clone of champion is added to each species
        for s in self.species:
            children.append(s.champion.clone())

        # Fill open player slots with children
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for s in self.species:
            for i in range(0, children_per_species):
                children.append(s.offspring())

        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.players = []
        for child in children:
            self.players.append(child)
        self.generation += 1

    # Return true if all players are dead
    def extinct(self):
        extinct = True
        for p in self.players:
            if p.alive:
                extinct = False
        return extinct
        
    def save_best_player(self):
        """Guardar el mejor jugador como un archivo CSV"""
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
            
            # Guardar información del modelo en un archivo de información
            with open(f'models/modelo{model_num}_info.txt', 'w') as f:
                f.write(f"Generaciones: {self.generation}\n")
                f.write(f"Fitness: {self.best_fitness}\n")
                f.write(f"Fecha de creacion: {import_datetime().now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Poblacion: {self.size}\n")
                f.write(f"Iteraciones: {self.iterations_limit}\n")
        else:
            print("No hay jugador para guardar")

def import_datetime():
    """Importa el módulo datetime solo cuando es necesario"""
    import datetime
    return datetime.datetime