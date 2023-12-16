import networkx as nx
import random

def generate_random_graph(N):
    G = nx.Graph()

    G.add_nodes_from(range(1, N + 1))

    # Add random edges between vertices
    for u in range(1, N + 1):
        for v in range(u + 1, N + 1):
            if random.choice([True, False]):
                G.add_edge(u, v)

    # Convert the graph to adjacency list format
    adjacency_list = {}
    for u in G.nodes():
        neighbors = sorted(G.neighbors(u))
        adjacency_list[u] = neighbors

    return adjacency_list

def print_adjacency_list(adjacency_list):
    for vertex, neighbors in adjacency_list.iteritems():
        print "{} {}".format(vertex, " ".join(map(str, neighbors)))

if __name__ == "__main__":
    N = 75  # Replace with the desired number of vertices
    random_graph = generate_random_graph(N)

    # print("Random Graph (Adjacency List):")
    print_adjacency_list(random_graph)
