import random

# Markov chain representation

# Define the graph in the terms of vertices
class Vertex(object):
    def __init__(self, value):#value will be the word
        self.value = value
        self.adjacent = {}  # nodes that it points to
        self.neighbors = []
        self.neighbors_weights = []

    def __str__(self):
        return self.value + ' '.join([node.value for node in self.adjacent.keys()])

    def add_edge_to(self, vertex, weight=0):
        self.adjacent[vertex] = weight

    def increment_edge(self, vertex):
        self.adjacent[vertex] = self.adjacent.get(vertex, 0) + 1

    # returns all the nodes that this vertex points to
    def get_adjacent_nodes(self):
        return self.adjacent.keys()

    # initializes probability map
    def get_probability_map(self):
        for (vertex, weight) in self.adjacent.items():#for each vertex and weight in the adjacent list
            self.neighbors.append(vertex)
            self.neighbors_weights.append(weight)

    def next_word(self):
        return random.choices(self.neighbors, weights=self.neighbors_weights)[0]#returns the next word


# Define the graph in the terms of vertices
class Graph(object):
    def __init__(self):
        self.vertices = {}

    # returns all the nodes in the graph
    def get_vertex_values(self):
        return set(self.vertices.keys())

    # add a new node to the graph
    def add_vertex(self, value):
        self.vertices[value] = Vertex(value)

    # get a node from the graph
    def get_vertex(self, value):
        if value not in self.vertices:#if the value is not in the graph
            self.add_vertex(value)#add the value to the graph
        return self.vertices[value]#return the value

    # returns the next word
    def get_next_word(self, current_vertex):
        return self.vertices[current_vertex.value].next_word()#returns the next word

    # generates probability mappings
    def generate_probability_mappings(self):
        for vertex in self.vertices.values():#for each vertex in the graph
            vertex.get_probability_map()#get the probability map
