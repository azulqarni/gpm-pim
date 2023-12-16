import os
import re
import matplotlib.pyplot as plt
import numpy as np

def extract_total_time(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        match = re.search(r'ramulator\.total_time\s+(\d+\.\d+)', content)
        if match:
            return float(match.group(1)) / 1e6  # Convert from ns to milliseconds
    return None

# List of benchmarks
benchmarks = ["trcount", "four-cliques", "five-cliques", "diamond-count", "four_cycles"]

# List of PIM cores
pim_cores = [4, 8, 16, 32, 48]

fig, axes = plt.subplots(nrows=len(benchmarks), ncols=1, figsize=(8, 6), sharex=True)

bar_width = 0.15
bar_positions = np.arange(len(pim_cores))

for i, benchmark in enumerate(benchmarks):
    data_exec_time = []

    for pim_core in pim_cores:
        file_path_exec_time = f"pim-{benchmark}-{pim_core}-threads.stats"
        exec_time = extract_total_time(file_path_exec_time)

        if exec_time is not None:
            data_exec_time.append(exec_time)

    # Plot Execution Time in the current subplot
    bars = axes[i].bar(bar_positions, data_exec_time, bar_width, label=f'{benchmark} - Execution Time', alpha=0.8, color='orange')

    # Plot Linear-Speedup Curve for Execution Time
    linear_speedup_exec_time = np.array([1, 1/2, 1/4, 1/8, 1/12]) * data_exec_time[0]
    axes[i].plot(bar_positions, linear_speedup_exec_time, marker='o', linestyle='-', color='red', label='Linear Speedup - Execution Time')

    # Print Peaks of the Bars for Execution Time
    for bar in bars:
        height = bar.get_height()
        axes[i].text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f} ms', ha='center', va='bottom')

    # Customize the subplot
    axes[i].legend()
    # axes[i].set_title(f'Execution Time (ms) for {benchmark} Benchmark')
    axes[0].set_title(f'Execution Time (ms)')

    # Expand y-axis range by 50%
    y_lower, y_upper = axes[i].get_ylim()
    y_range = y_upper - y_lower
    axes[i].set_ylim(y_lower, y_upper + 0.8 * y_range)

# Customize the overall plot
plt.xlabel('Number of PIM Cores')
plt.xticks(bar_positions, pim_cores)  # Add this line to set x-axis labels
fig.text(0.04, 0.5, ' ', va='center', rotation='vertical', ha='center', fontsize=12)  # Common ylabel for all subplots
# plt.tight_layout()

plt.savefig('execution_time_plot.pdf')

