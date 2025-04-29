import math  # Importamos el módulo math para la función exponencial (exp)

class Node:
    """
    La clase Node representa un nodo (neurona) en la red neuronal.
    Cada nodo puede recibir entradas, procesarlas y enviar su salida a otros nodos.
    """
    def __init__(self, id_number):
        """
        Inicializa un nodo con sus propiedades básicas.
        
        Args:
            id_number: Identificador único del nodo
        """
        self.id = id_number              # Identificador único del nodo
        self.layer = 0                   # Capa a la que pertenece (0=entrada, 1=salida)
        self.input_value = 0             # Valor de entrada acumulado desde conexiones entrantes
        self.output_value = 0            # Valor de salida (resultado de la función de activación)
        self.connections = []            # Lista de conexiones salientes desde este nodo
    
    def activate(self):
        """
        Activa el nodo aplicando la función de activación y propaga el resultado.
        Para nodos de salida, aplica la función sigmoide al valor de entrada.
        Para nodos de entrada, el output_value ya está establecido directamente.
        """
        # Función sigmoide: transforma cualquier valor en un número entre 0 y 1
        def sigmoid(x):
            return 1/(1+math.exp(-x))
        
        # Solo los nodos de salida (capa 1) aplican la función de activación
        if self.layer == 1:
            self.output_value = sigmoid(self.input_value)
        
        # Propagar la salida a todos los nodos conectados
        for i in range(0, len(self.connections)):
            # Cada conexión transmite: salida del nodo * peso de la conexión
            self.connections[i].to_node.input_value += \
                self.connections[i].weight * self.output_value
    
    def clone(self):
        """
        Crea una copia exacta del nodo, utilizada durante la reproducción.
        
        Returns:
            Un nuevo nodo con el mismo ID y capa que este nodo
        """
        clone = Node(self.id)    # Crear nuevo nodo con el mismo ID
        clone.id = self.id       # Establecer ID
        clone.layer = self.layer # Copiar capa
        return clone             # Devolver el clon