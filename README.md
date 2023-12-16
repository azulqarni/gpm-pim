# Using Near-data Processing (NDP) for Graph Pattern Mining (GPM) Applications

In this project, we evaluate the scalability of NDP architectures for a varying NDP number of over implementations of common GPM the benchmarks provided in this repository.

## Building the Benchmarks
The benchmakrs are located inside [gpm-pim/benchmarks/graph_mining](https://github.com/azulqarni/gpm-pim/tree/main/benchmarks/graph_mining) and rely on the OpenMP API for multithreading.
1) In the `Makefile`, set the parameter `-DNUM_THREADS=1` appropriately to enable a respective amount of threads to be used for each application
2) Use `make` to build the benchmarks.
3) Use `graphgen.py` to generate random graphs of N nodes; N may provided as command line argument. The subfolder `data` contains some input graphs in the adjacency list format.

## Running the Simulations

1) You will first need to build ZSim+Ramulator [Ramulator-PIM repository](https://github.com/CMU-SAFARI/ramulator-pim).
3) To obtain memory traces from the benchmarks using ZSim, run `batch_sims.sh`.
   - Make sure to update the executable path @line 15.
   - Note that this script modifies the ZSim configuration files in `tests` folder, accordingly.
4) Inspect `ramulator-Configs/pim.cfg` file with the specification of the simulated memory system's parameters.
5) To feed the obtained memory traces to Ramulator, run `run_sims.sh`. Example traces are included inside `sims.16threads`.
   - Make sure to specify how many cores does the experiment you run simulate e.g., via command line argument or via the default value @line 3
   - Make sure to update (if necessary) the memory traces path @line 14.
6) To plot the Ramulator generated statistics, use the python scripts in the `stats` folder. Example stats are provided inside `stats` folder.
