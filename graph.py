class Graph:
    #initialiser la classe Graph avec pour attribut node (noeuds) ensemble vide et edge (arrêtes) dictionnaire vide
    def __init__(self):
        self.nodes = set()
        self.edges = {}

    #Méthode pour rajouter des noeuds 
    def add_node(self, node):
        self.nodes.add(node)

    #Méthode pour rajouter des arrêtes avec pour paramètre from_node(noeud de départ), to_node(noeud d'arriver) et weight (poids)
    def add_edge(self, from_node, to_node, weight):
        if from_node not in self.edges:
            self.edges[from_node] = {}
        if to_node not in self.edges:
            self.edges[to_node] = {}
        self.edges[from_node][to_node] = weight
        self.edges[to_node][from_node] = weight 

    #Méthode de bellman_ford permattant de trouver le chemin le plus court en renvoyant le temps et le chemin en sortie de méthode
    def bellman_ford(self, start):
        distance = {node: float('inf') for node in self.nodes}
        distance[start] = 0
        path = {node: [] for node in self.nodes}  
        path[start] = [start]
        for _ in range(len(self.nodes) - 1):
            for node in self.nodes:
                for neighbour in self.edges[node].keys():
                    new_distance = distance[node] + self.edges[node][neighbour]
                    if new_distance < distance[neighbour]:
                        distance[neighbour] = new_distance
                        path[neighbour] = path[node] + [neighbour] 
        distance = {node: round(distance[node] / 60) for node in distance}
        return distance, path 
