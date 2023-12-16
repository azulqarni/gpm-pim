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

// Function to count 4-cycles in a graph
int count_4cycles_parallel(const Graph& G) {
    zsim_roi_begin();
    int num_fourcycle = 0;

    #pragma omp parallel for shared(G) schedule(dynamic) reduction(+:num_fourcycle)
    for (int i = 0; i < G.vertices.size(); ++i) {
        int u0 = G.vertices[i];
        const auto& Nu0 = G.out_neighbors(u0);

        // #pragma omp parallel for shared(u0, Nu0) firstprivate(num_fourcycle) schedule(dynamic)
        for (int j = 0; j < Nu0.size(); ++j) {
            zsim_PIM_function_begin();
            int u1 = Nu0[j];
            if (u1 >= u0) {
                continue;
            }
            // zsim_PIM_function_end();

            const auto& Nu1 = G.out_neighbors(u1);


            // #pragma omp parallel for shared(u0, u1, Nu0, Nu1) firstprivate(num_fourcycle) schedule(dynamic)
            for (int k = 0; k < Nu0.size(); ++k) {
                // zsim_PIM_function_begin();
                int u2 = Nu0[k];
                if (u2 >= u1) {
                    continue;
                }

                const auto& Nu2 = G.out_neighbors(u2);

                auto Nu1u2 = vector_intersection(Nu1, Nu2);

                // #pragma omp parallel for shared(u0, u1, u2, Nu0, Nu1, Nu2, Nu1u2) firstprivate(num_fourcycle) schedule(dynamic)
                for (int l = 0; l < Nu1u2.size(); ++l) {
                    int u3 = Nu1u2[l];
                    if (u3 >= u0) {
                        continue;
                    }
                    #pragma omp atomic
                    num_fourcycle++;
                }
                // zsim_PIM_function_end();
            }
            zsim_PIM_function_end();
        }
    }
    zsim_roi_end();

    return num_fourcycle;
}

int main(int argc, char *argv[]) {

    omp_set_num_threads(NUM_THREADS);

    Graph G;
    G.loadFromFile(argv[1]);

    int result = count_4cycles_parallel(G);
    std::cout << "Number of 4-cycles: " << result << std::endl;

    return 0;
}
