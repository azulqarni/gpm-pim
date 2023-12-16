#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <omp.h>
#include "../../misc/hooks/zsim_hooks.h"

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

// Function to count diamonds in a graph
int countDiamonds(const Graph& graph) {
    int numDiamonds = 0;
    zsim_roi_begin();
    #pragma omp parallel for shared(graph) reduction(+:numDiamonds)
    for (int i = 0; i < graph.vertices.size(); ++i) {
        int u0 = graph.vertices[i];
        const std::vector<int>& Nu0 = graph.out_neighbors(u0);
        zsim_PIM_function_begin();
        for (int j = 0; j < Nu0.size(); ++j) {
            int u1 = Nu0[j];
            if (u1 >= u0) {
                continue;
            }

            const std::vector<int>& Nu1 = graph.out_neighbors(u1);
            std::vector<int> Nu0u1 = vector_intersection(Nu0, Nu1);

            for (int k = 0; k < Nu0u1.size(); ++k) {
                int u2 = Nu0u1[k];

                // #pragma omp parallel for firstprivate(u0, u1, u2) shared(graph) reduction(+:numDiamonds)
                for (int l = 0; l < Nu0u1.size(); ++l) {
                    int u3 = Nu0u1[l];
                    if (u3 >= u2) {
                        continue;
                    }

                    numDiamonds++;
                }
            }
        }
        zsim_PIM_function_end();
    }
    zsim_roi_end();
    return numDiamonds;
}

int main(int argc, char *argv[]) {
    omp_set_num_threads(NUM_THREADS);

    Graph G;
    G.loadFromFile(argv[1]);

    // Count diamonds in the graph
    int result = countDiamonds(G);
    std::cout << "Number of diamonds in the graph: " << result << std::endl;

    return 0;
}
