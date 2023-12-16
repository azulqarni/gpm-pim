#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <algorithm>
#include <functional>
#include <omp.h>
#include "../../misc/hooks/zsim_hooks.h"

#ifndef K
#define K 4
#endif

#ifndef NUM_THREADS
#define NUM_THREADS 4
#endif

class Graph {
public:
    std::vector<int> vertices;
    std::unordered_map<int, std::vector<int>> adjacency_list;

    std::vector<int> out_neighbors(int u) const {
        auto it = adjacency_list.find(u);
        if (it != adjacency_list.end()) {
            return it->second;
        } else {
            return {};
        }
    }

    // Method to load a graph from a file containing an adjacency list
    void loadFromFile(const std::string& filename) {
        std::ifstream file(filename);
        if (file.is_open()) {
            std::string line;
            while (std::getline(file, line)) {
                std::istringstream iss(line);
                int vertex;
                iss >> vertex;

                int neighbor;
                std::vector<int> neighbors;

                while (iss >> neighbor) {
                    neighbors.push_back(neighbor);
                }

                adjacency_list[vertex] = neighbors;
                vertices.push_back(vertex);
            }

            file.close();
        } else {
            std::cerr << "Unable to open file: " << filename << std::endl;
        }
    }
};

// Function to find the intersection of two vectors
std::vector<int> vector_intersection(const std::vector<int>& v1, const std::vector<int>& v2) {
    std::vector<int> result;
    for (int value : v1) {
        if (std::find(v2.begin(), v2.end(), value) != v2.end()) {
            result.push_back(value);
        }
    }
    return result;
}

int count_k_cliques_old(const Graph& graph, int k) {
    int ck = 0;
    zsim_roi_begin();
    // Function to recursively count k-cliques
    std::function<int(int, const std::vector<int>&)> count_cliques = [&](int i, const std::vector<int>& current_clique) -> int {
        if (i == k) {
            return 1;  // Count k-cliques
        } else {
            int ci = 0;

            #pragma omp parallel for reduction(+:ci) shared(graph, current_clique)
            for (size_t j = 0; j < current_clique.size(); ++j) {
                zsim_PIM_function_begin();
                int v = current_clique[j];
                // Search within the neighborhood of 𝑣
                std::vector<int> next_clique = vector_intersection(graph.out_neighbors(v), current_clique);
                ci += count_cliques(i + 1, next_clique);
                zsim_PIM_function_end();
            }

            return ci;
        }
    };


    // Iterate over vertices to count k-cliques
    #pragma omp parallel for reduction(+:ck) shared(graph)
    for (size_t i = 0; i < graph.vertices.size(); ++i) {
        zsim_PIM_function_begin();
        int u = graph.vertices[i];
        std::vector<int> C2 = graph.out_neighbors(u);
        ck += count_cliques(2, C2);
        zsim_PIM_function_end();
    }
    zsim_roi_end();

    return ck;
}

// Recursive function to count k-cliques
int count_cliques_recursive(const Graph& graph, int k, int i, const std::vector<int>& current_clique) {
    if (i == k) {
        return 1;  // Count k-cliques
    } else {
        int ci = 0;
        // #pragma omp parallel for reduction(+:ci) shared(graph, current_clique)
        for (size_t j = 0; j < current_clique.size(); ++j) {
            int v = current_clique[j];
            std::vector<int> next_clique = vector_intersection(graph.out_neighbors(v), current_clique);
            ci += count_cliques_recursive(graph, k, i + 1, next_clique);
        }

        return ci;
    }
}

int count_k_cliques(const Graph& graph, int k) {
    zsim_roi_begin();
    int ck = 0;

    #pragma omp parallel for reduction(+:ck) shared(graph)
    for (size_t i = 0; i < graph.vertices.size(); ++i) {
        zsim_PIM_function_begin();
        int u = graph.vertices[i];
        std::vector<int> C2 = graph.out_neighbors(u);
        ck += count_cliques_recursive(graph, k, 2, C2);
    }
    zsim_PIM_function_end();

    zsim_roi_end();

    return ck;
}

int main(int argc, char *argv[]) {
    omp_set_num_threads(NUM_THREADS);

    Graph graph;
    graph.loadFromFile(argv[1]);

    int k_value = K;
    int result = count_k_cliques(graph, k_value);
    std::cout << "Number of " << k_value << "-cliques: " << result << std::endl;

    return 0;
}
