import os
import re
import matplotlib.pyplot as plt
import numpy as np

def extract_bandwidth_metrics(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        read_bandwidth_match = re.search(r'ramulator\.read_bandwidth\s+(\d+)', content)
        write_bandwidth_match = re.search(r'ramulator\.write_bandwidth\s+(\d+)', content)
        max_internal_bandwidth_match = re.search(r'ramulator\.maximum_internal_bandwidth\s+(\d+)', content)

        if read_bandwidth_match and write_bandwidth_match and max_internal_bandwidth_match:
            read_bandwidth = float(read_bandwidth_match.group(1)) / (1024 ** 3)  # Convert from Bps to GB/s
            write_bandwidth = float(write_bandwidth_match.group(1)) / (1024 ** 3)  # Convert from Bps to GB/s
            max_internal_bandwidth = float(max_internal_bandwidth_match.group(1)) / (1024 ** 3)  # Convert from Bps to GB/s

            return ((read_bandwidth + write_bandwidth) / max_internal_bandwidth) * 100

    return None

# List of benchmarks
benchmarks = ["trcount", "four-cliques", "five-cliques", "diamond-count", "four_cycles"]

# List of PIM cores
pim_cores = [4, 8, 16, 32, 48]

# Set up subplots
fig, axes = plt.subplots(nrows=len(benchmarks), ncols=1, figsize=(8, 10), sharex=True)

# Plot the data and linear-speedup curves
bar_width = 0.15
bar_positions = np.arange(len(pim_cores))

for i, benchmark in enumerate(benchmarks):
    data_utilization = []

    # Iterate through PIM cores
    for pim_core in pim_cores:
        file_path = f"pim-{benchmark}-{pim_core}-threads.stats"
        utilization = extract_bandwidth_metrics(file_path)

        if utilization is not None:
            data_utilization.append(utilization)

    # Plot Bandwidth Utilization in the current subplot
    bars = axes[i].bar(bar_positions, data_utilization, bar_width, label=f'{benchmark}', alpha=0.8)

    # Plot Linear-Speedup Curve
    linear_speedup_points = np.array([1, 2, 4, 8, 12]) * data_utilization[0]
    axes[i].plot(bar_positions, linear_speedup_points, marker='o', linestyle='-', color='black', label='Linear Speedup')

    # Print Peaks of the Bars
    for bar in bars:
        height = bar.get_height()
        axes[i].text(bar.get_x() + bar.get_width() / 2, height, f'{height:.3f}%', ha='center', va='bottom')

    # Print Points of the Linear-Speedup Curve
    # for x, y in zip(bar_positions, linear_speedup_points):
        # axes[i].text(x, y, f'({x}, {y:.2f}%)', ha='right', va='bottom')

    # Customize the subplot
    # axes[i].set_ylabel('Bandwidth Utilization (%)')
    axes[i].legend()
    # axes[i].set_title(f'Bandwidth Utilization (%) for {benchmark} Benchmark')
    axes[0].set_title(f'Bandwidth Utilization (%)')

# Customize the overall plot
plt.xlabel('Number of PIM Cores')
plt.xticks(bar_positions, pim_cores)  # Add this line to set x-axis labels
plt.tight_layout()

# Save the plot as a PDF file
plt.savefig('bandwidth_utilization_plot.pdf')

# Optionally, you can display the plot if needed
# plt.show()
