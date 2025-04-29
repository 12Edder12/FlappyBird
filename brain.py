import node  # Importa el módulo que define los nodos de la red neuronal
import connection  # Importa el módulo que define las conexiones entre nodos
import random  # Para generar valores aleatorios en los pesos iniciales


class Brain:
    """
    La clase Brain implementa una red neuronal simple de topología fija.
    Representa el cerebro de cada jugador (pájaro) y toma decisiones basadas en la información visual.
    """
    def __init__(self, inputs, clone=False):
        """
        Inicializa la red neuronal.
        
        Args:
            inputs: Número de nodos de entrada (sensores de visión del pájaro)
            clone: Bandera que indica si este cerebro es un clon (para reproducción)
        """
        self.connections = []  # Lista de conexiones entre nodos
        self.nodes = []  # Lista de todos los nodos en la red
        self.inputs = inputs  # Número de entradas (3 en este caso)
        self.net = []  # Lista ordenada de nodos para propagación hacia adelante
        self.layers = 2  # Número de capas en la red (entrada y salida)

        # Si no es un clon, crear una nueva red desde cero
        if not clone:
            # Crear nodos de entrada (3 nodos para las distancias a las tuberías)
            for i in range(0, self.inputs):
                self.nodes.append(node.Node(i))  # Crear un nodo con ID único
                self.nodes[i].layer = 0  # Todos en la capa 0 (entrada)
                
            # Crear nodo de sesgo (bias) siempre con valor 1
            self.nodes.append(node.Node(3))
            self.nodes[3].layer = 0  # También en la capa de entrada
            
            # Crear nodo de salida (decide si aletear o no)
            self.nodes.append(node.Node(4))
            self.nodes[4].layer = 1  # En la capa 1 (salida)

            # Crear conexiones: cada nodo de entrada conecta directamente al nodo de salida
            for i in range(0, 4):  # Para los 3 nodos de entrada + nodo bias
                # Crear conexión con peso aleatorio entre -1 y 1
                self.connections.append(connection.Connection(
                    self.nodes[i],  # Nodo de origen
                    self.nodes[4],  # Nodo de destino (salida)
                    random.uniform(-1, 1)  # Peso aleatorio inicial
                ))

    def connect_nodes(self):
        """
        Establece las conexiones entre nodos.
        Cada nodo mantiene una lista de conexiones salientes desde él.
        """
        # Limpiar listas de conexiones previas
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []

        # Agregar cada conexión a la lista del nodo de origen
        for i in range(0, len(self.connections)):
            self.connections[i].from_node.connections.append(self.connections[i])

    def generate_net(self):
        """
        Prepara la red para hacer propagación hacia adelante.
        Ordena los nodos por capas para procesamiento secuencial.
        """
        self.connect_nodes()  # Primero establecer las conexiones
        self.net = []  # Reiniciar la lista de nodos ordenados
        
        # Recorrer cada capa y añadir sus nodos a la lista ordenada
        for j in range(0, self.layers):
            for i in range(0, len(self.nodes)):
                if self.nodes[i].layer == j:
                    self.net.append(self.nodes[i])

    def feed_forward(self, vision):
        """
        Realiza la propagación hacia adelante en la red neuronal.
        
        Args:
            vision: Lista con los valores de entrada (distancias normalizadas)
            
        Returns:
            Valor de salida del nodo final (entre 0 y 1)
        """
        # Establecer los valores de entrada (visión) en los nodos de entrada
        for i in range(0, self.inputs):
            self.nodes[i].output_value = vision[i]

        # El nodo bias siempre tiene valor 1
        self.nodes[3].output_value = 1

        # Activar todos los nodos en orden por capas
        for i in range(0, len(self.net)):
            self.net[i].activate()  # Cada nodo sumará sus entradas y aplicará función sigmoide

        # Obtener el valor de salida del nodo final
        output_value = self.nodes[4].output_value

        # Reiniciar los valores de entrada para la próxima iteración
        for i in range(0, len(self.nodes)):
            self.nodes[i].input_value = 0

        return output_value  # Retorna valor entre 0 y 1

    def clone(self):
        """
        Crea una copia exacta de este cerebro.
        Utilizado en el proceso de reproducción y evolución.
        
        Returns:
            Un nuevo objeto Brain que es copia de este
        """
        clone = Brain(self.inputs, True)  # Crear cerebro vacío

        # Clonar todos los nodos
        for n in self.nodes:
            clone.nodes.append(n.clone())

        # Clonar todas las conexiones
        # Nota: Debemos asegurarnos de que las conexiones apunten a los nodos del clon, no del original
        for c in self.connections:
            clone.connections.append(c.clone(
                clone.getNode(c.from_node.id),  # Buscar nodo de origen en el clon
                clone.getNode(c.to_node.id)     # Buscar nodo de destino en el clon
            ))

        clone.layers = self.layers
        clone.connect_nodes()  # Establecer conexiones en el clon
        return clone

    def getNode(self, id):
        """
        Busca un nodo por su ID.
        
        Args:
            id: Identificador único del nodo
            
        Returns:
            El nodo con ese ID o None si no se encuentra
        """
        for n in self.nodes:
            if n.id == id:
                return n
        return None

    def mutate(self):
        """
        Aplica mutación a las conexiones de la red.
        80% de probabilidad de que ocurra mutación.
        Parte fundamental del algoritmo genético.
        """
        if random.uniform(0, 1) < 0.8:  # 80% de probabilidad de mutación
            # Mutar todos los pesos de las conexiones
            for i in range(0, len(self.connections)):
                self.connections[i].mutate_weight()  # Cada conexión aplica su propia lógica de mutación