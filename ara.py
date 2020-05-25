from binary_heap import BinaryHeap
from node import Node
import time


class Ara:
    def __init__(self, initial_state, heuristic, weight=1, max_expansions=80000):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.heuristic = heuristic
        self.weight = weight
        self.max_expansions = max_expansions

    def estimate_suboptimality(self, result):
        costo = result.g
        mini = 1000000000
        for n in self.open:
            f = n.h + n.g
            if f < mini:
                mini = f
        return costo/mini


        print(self.open)

        return 0  # este método debe ser implementado en la parte 1

    def fvalue(self, g, h):
        return (g + self.weight*h, h) #Esto nos permite seleccionar primero los que tienen menor h si g+h spn iguales

    def update_weight(self, n):
        new_weight = self.estimate_suboptimality(n)
        self.weight = new_weight
        for node in self.open:
            node.key = self.fvalue(node.g, node.h)
        self.open.reorder()
    def search(self):
        cult = 10000000000
        self.start_time = time.process_time()
        self.open = BinaryHeap()
        self.expansions = 0
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.heuristic(self.initial_state)
        initial_node.key = self.fvalue(0, initial_node.h) # asignamos el valor f
        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        while not self.open.is_empty() and self.expansions <= self.max_expansions:
            n = self.open.extract()   # extrae n de la open
            if n.state.is_goal():
                self.end_time = time.process_time()
                yield n
                self.update_weight(n)
                cult = n.g
            succ = n.state.successors()
            self.expansions += 1
            for child_state, action, cost in succ:
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if (is_new or path_cost < child_node.g) and path_cost < cult:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = Node(child_state, n)
                        child_node.h = self.heuristic(child_state)
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.key = self.fvalue(child_node.g, child_node.h) # actualizamos el valor f de child_node
                    self.open.insert(child_node) # inserta child_node a la open si no esta en la open
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        if self.open.is_empty():
            yield n
