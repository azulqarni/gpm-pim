# C compiler
CC = g++
ICC = /opt/intel/oneapi/compiler/2024.0/bin/icpx #icc
CC_FLAGS = -pg -fopenmp -O2 -DNUM_THREADS=1
ICC_FLAGS = -g -qopenmp -O2

all: trcount_offload five_cliques_offload four_cliques_offload four_cycles_offload diamond_counting_offload

diamond_counting_offload: diamond-counting.cpp
	$(CC) $(CC_FLAGS) -DOMP_OFFLOAD diamond-counting.cpp -o diamond_counting_offload

four_cycles_offload: four-cycles.cpp
	$(CC) $(CC_FLAGS) -DOMP_OFFLOAD four-cycles.cpp -o four_cycles_offload

five_cliques_offload: k-cliques.cpp
	$(CC) $(CC_FLAGS) -DK=5 -DOMP_OFFLOAD k-cliques.cpp -o five_cliques_offload

four_cliques_offload: k-cliques.cpp
	$(CC) $(CC_FLAGS) -DK=4 -DOMP_OFFLOAD k-cliques.cpp -o four_cliques_offload

trcount_offload: trcount.cpp
	$(CC) $(CC_FLAGS) -DOMP_OFFLOAD trcount.cpp -o trcount_offload

clean:
	rm -f trcount_offload *_cliques_offload four_cycles_offload diamond_counting_offload
