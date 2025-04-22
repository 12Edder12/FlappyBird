import random


class Connection:
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.enabled = True

    def mutate_weight(self):
        # 10% chance to completely change the weight
        if random.uniform(0, 1) < 0.1:
            self.weight = random.uniform(-1, 1)
        else:  # Otherwise slightly adjust it
            self.weight += random.gauss(0, 1) / 50
            # Keep weight in proper range
            if self.weight > 1:
                self.weight = 1
            if self.weight < -1:
                self.weight = -1

    def clone(self, from_node, to_node):
        clone = Connection(from_node, to_node, self.weight)
        clone.enabled = self.enabled
        return clone