import os
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

def extract_total_time(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        match = re.search(r'ramulator\.total_time\s+(\d+\.\d+)', content)
        if match:
            return float(match.group(1)) / 1e6  # Convert from ns to milliseconds
    return None

# List of benchmarks
benchmarks = ["trcount", "four-cliques", "diamond-count", "four_cycles"] # Exclude "five-cliques", because it causes scaling issues
benchmarks = ["five-cliques"]

# List of PIM cores
pim_cores = [4, 8, 16, 32, 48]

# Initialize data for plotting
data = {benchmark: [] for benchmark in benchmarks}

# Iterate through benchmarks
for benchmark in benchmarks:
    total_time_values = []

    # Iterate through PIM cores
    for pim_core in pim_cores:
        file_path = f"pim-{benchmark}-{pim_core}-threads.stats"
        total_time = extract_total_time(file_path)

        if total_time is not None:
            total_time_values.append(total_time)

    data[benchmark] = total_time_values

# Plot the data with a denser and darker blue spectrum
bar_width = 0.15
bar_positions = np.arange(len(benchmarks))

norm = Normalize(vmin=min(pim_cores), vmax=max(pim_cores))
sm = ScalarMappable(cmap='Blues_r', norm=norm)  # Reversed spectrum for darker colors
sm.set_array([])

# for i, pim_core in enumerate(pim_cores):
#     plt.bar(bar_positions + i * bar_width, [data[benchmark][i] for benchmark in benchmarks], bar_width,
#             label=f'{pim_core} Cores', color=sm.to_rgba(pim_core))

for i, pim_core in enumerate(pim_cores):
    color = sm.to_rgba(pim_core)
    # reversed_color = (color[2], color[1], color[0], color[3])  # Reverse the order of RGB values

    # if pim_core == max(pim_cores):
        # Manually set a darker color for the rightmost bar
        # reversed_color = (reversed_color[0] * 0.7, reversed_color[1] * 0.7, reversed_color[2] * 0.7, reversed_color[3])

    # if pim_core == min(pim_cores):
        # Manually set a darker color for the rightmost bar
        # reversed_color = (reversed_color[0] * 0.7, reversed_color[1] * 0.7, reversed_color[2] * 0.7, reversed_color[3])

    plt.bar(bar_positions + i * bar_width, [data[benchmark][i] for benchmark in benchmarks], bar_width,
            label=f'{pim_core} Cores', color=color)

# Customize the plot
plt.xlabel('Benchmarks')
plt.ylabel('Total Time (ms)')
plt.title('Total Time Performance for Different Benchmarks and PIM Cores')
plt.xticks(bar_positions + (len(pim_cores) - 1) * bar_width / 2, benchmarks)
plt.legend(title='Number of Cores')
plt.tight_layout()

# Save the plot as a PDF file
plt.savefig('total_time_performance_plot.svg')

# Optionally, you can display the plot if needed
# plt.
