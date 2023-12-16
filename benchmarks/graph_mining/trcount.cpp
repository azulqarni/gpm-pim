#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
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

void print_set(const std::vector<int>& s) {
    std::cout << "{ ";
    for (int elem : s) {
        std::cout << elem << " ";
    }
    std::cout << "}" << std::endl;
}

int set_intersection(const std::vector<int>& SetA, const std::vector<int>& SetB, std::vector<int>& intersection_result) {
    auto itA = SetA.begin();
    auto itB = SetB.begin();

    while (itA != SetA.end() && itB != SetB.end()) {
        if (*itA < *itB) {
            ++itA;
        } else if (*itA > *itB) {
            ++itB;
        } else {
            intersection_result.push_back(*itA);
            ++itA;
            ++itB;
        }
    }

    return intersection_result.size();
}

int GPM_TC(const Graph& G, const Graph& P) {
    int num_triangles = 0;

    zsim_roi_begin();
    #pragma omp parallel for schedule(dynamic) reduction(+:num_triangles)
    for (int u = 0; u < G.vertices.size(); ++u) {
        auto N_u = G.out_neighbors(u);
        int* N_u_array = N_u.data();  // Copy N_u to an array

        #pragma omp target data map(to: N_u_array[:N_u.size()]) map(from: num_triangles)
        {
            for (int v = 0; v < N_u.size(); ++v) {
                zsim_PIM_function_begin();
                if (N_u_array[v] >= u) {
                    continue;
                }

                auto N_v = G.out_neighbors(N_u_array[v]);
                std::vector<int> N_u_v;
                set_intersection(N_u, N_v, N_u_v);

                for (int w = 0; w < N_u_v.size(); ++w) {
                    if (N_u_v[w] >= N_u_array[v]) {
                        continue;
                    }

                    #pragma omp atomic
                    num_triangles++;
                }
                zsim_PIM_function_end();
            }
        }
    }

    zsim_roi_end();
    return num_triangles;
}

int main(int argc, char *argv[]) {
    omp_set_num_threads(NUM_THREADS);

    Graph G;

    G.loadFromFile(argv[1]);

    int result = GPM_TC(G, G);

    std::cout << "Number of triangles: " << result << std::endl;

    return 0;
}
