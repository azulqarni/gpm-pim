#!/bin/bash

# List of configuration files
config_files=(
    "pim_diamond_count.cfg"
    "pim_five_cliques.cfg"
    "pim_four_cliques.cfg"
    "pim_four_cycle_count.cfg"
    "pim_trcount.cfg"
)

export cores=48

# Path to the executable
export executable="./build/opt/zsim"

# Define a function to process each configuration file
process_config_file() {
    config_file=$1

    # Replace the RHS with the variable
    sed -i "s/\(cores[[:space:]]*=[[:space:]]*\)[0-9]\+/\1$cores/" "tests/$config_file"
    sed -i "/caches[[:space:]]*=[[:space:]]*1;/! s/\(caches[[:space:]]*=[[:space:]]*\)[0-9]\+/\\1$cores/" "tests/$config_file"

    command="$executable tests/$config_file"

    echo "Running: $command"

    $command

    echo "----------------------------------------"
}

# Export the function so that it's available to parallel
export -f process_config_file

# Use parallel to run the function in parallel for each configuration file
parallel -j 2 process_config_file ::: "${config_files[@]}"
