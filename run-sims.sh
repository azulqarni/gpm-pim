#!/bin/bash

default_cores=4
export cores=${1:-$default_cores} && echo "Number of cores set to: $cores"
export traces=sims.${cores}threads

# Function to run a single simulation
run_simulation() {
    sim=$1
    ./ramulator --config Configs/pim.cfg \
    --disable-perf-scheduling true \
    --mode=cpu \
    --stats pim-${sim}-${cores}-threads.stats \
    --trace ../zsim-ramulator/sims.${cores}threads/${sim}.out \
    --core-org=outOrder \
    --number-cores=$cores \
    --trace-format=zsim \
    --split-trace=true
}

export -f run_simulation

# List of simulations
simulations=("pim-diamond-count" "pim-five-cliques" "pim-four-cliques" "pim-four_cycles" "pim-trcount")

# Run simulations in parallel
parallel -j 4 run_simulation ::: "${simulations[@]}"
