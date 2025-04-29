import random  # Para generar valores aleatorios en las mutaciones


class Connection:
    """
    La clase Connection representa una conexión entre dos nodos en la red neuronal.
    Contiene un peso que determina la importancia de la señal transmitida.
    """
    
    def __init__(self, from_node, to_node, weight):
        """
        Inicializa una conexión entre dos nodos con un peso específico.
        
        Args:
            from_node: Nodo de origen (el que envía la señal)
            to_node: Nodo de destino (el que recibe la señal)
            weight: Valor que determina la importancia/influencia de esta conexión
        """
        self.from_node = from_node  # Nodo de origen
        self.to_node = to_node      # Nodo de destino
        self.weight = weight        # Peso de la conexión (entre -1 y 1)
        self.enabled = True         # Indica si la conexión está activa

    def mutate_weight(self):
        """
        Muta (modifica) el peso de la conexión.
        Esta función es clave para el algoritmo genético, permitiendo explorar nuevas soluciones.
        Hay dos tipos de mutación posibles:
        1. Cambio completo (10% de probabilidad): Asigna un nuevo peso aleatorio
        2. Ajuste ligero (90% de probabilidad): Modifica ligeramente el peso existente
        """
        # 10% de probabilidad de cambio completo del peso
        if random.uniform(0, 1) < 0.1:
            self.weight = random.uniform(-1, 1)  # Nuevo peso aleatorio entre -1 y 1
        else:  # 90% de probabilidad de ajuste ligero
            # Añadir una pequeña variación gaussiana (centrada en 0)
            self.weight += random.gauss(0, 1) / 50
            
            # Mantener el peso en el rango adecuado (-1 a 1)
            if self.weight > 1:
                self.weight = 1
            if self.weight < -1:
                self.weight = -1

    def clone(self, from_node, to_node):
        """
        Crea una copia exacta de esta conexión, pero con nodos específicos.
        Utilizado durante la reproducción para crear copias de las conexiones.
        
        Args:
            from_node: Nodo de origen para la conexión clonada
            to_node: Nodo de destino para la conexión clonada
            
        Returns:
            Una nueva conexión con el mismo peso pero entre los nodos especificados
        """
        clone = Connection(from_node, to_node, self.weight)  # Crear nueva conexión
        clone.enabled = self.enabled  # Copiar estado de activación
        return clone  # Retornar el clon