import os
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize, PowerNorm

def extract_read_bandwidth(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        match = re.search(r'ramulator\.read_bandwidth\s+(\d+)', content)
        if match:
            return float(match.group(1)) / (1024 ** 3)  # Convert from Bps to GB/s
    return None

# List of benchmarks
benchmarks = ["trcount", "four-cliques", "diamond-count", "four_cycles"]
benchmarks = ["five-cliques"]

# List of PIM cores
pim_cores = [4, 8, 16, 32, 48]

# Initialize data for plotting
data = {benchmark: [] for benchmark in benchmarks}

# Iterate through benchmarks
for benchmark in benchmarks:
    read_bandwidth_values = []

    # Iterate through PIM cores
    for pim_core in pim_cores:
        file_path = f"pim-{benchmark}-{pim_core}-threads.stats"
        read_bandwidth = extract_read_bandwidth(file_path)

        if read_bandwidth is not None:
            read_bandwidth_values.append(read_bandwidth)

    data[benchmark] = read_bandwidth_values

# Plot the data with a denser and reversed blue spectrum
bar_width = 0.15
bar_positions = np.arange(len(benchmarks))

norm = PowerNorm(0.3, vmin=min(pim_cores), vmax=max(pim_cores))
sm = ScalarMappable(cmap='Blues', norm=norm)  # Use the original 'Blues' colormap
sm.set_array([])

for i, pim_core in enumerate(pim_cores):
    color = sm.to_rgba(pim_core)
    # color = (color[2], color[1], color[0], color[3])  # Reverse the order of RGB values

    if pim_core == max(pim_cores):
        # Manually set a darker color for the rightmost bar
        color = (color[0] * 0.7, color[1] * 0.7, color[2] * 0.7, color[3])

    # if pim_core == min(pim_cores):
    #     # Manually set a darker color for the rightmost bar
    #     color = (color[0] * 0.7, color[1] * 0.7, color[2] * 0.7, color[3])

    plt.bar(bar_positions + i * bar_width, [data[benchmark][i] for benchmark in benchmarks], bar_width,
            label=f'{pim_core} Cores', color=color)

# Customize the plot
plt.xlabel('Benchmarks')
plt.ylabel('Read Bandwidth (GB/s)')
plt.title('Read Bandwidth Performance for Different Benchmarks and PIM Cores')
plt.xticks(bar_positions + (len(pim_cores) - 1) * bar_width / 2, benchmarks)
plt.legend(title='Number of Cores')
plt.tight_layout()

# Save the plot as a PDF file
plt.savefig('read_bandwidth_performance_plot.svg')

# Optionally, you can display the plot if needed
# plt.show()
