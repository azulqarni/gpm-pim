import os
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

def extract_ipc(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        match = re.search(r'ramulator\.ipc\s+(\d+\.\d+)', content)
        if match:
            return float(match.group(1))
    return None

# List of benchmarks
benchmarks = ["trcount", "four-cliques", "five-cliques", "diamond-count", "four_cycles"]

# List of PIM cores
pim_cores = [4, 8, 16, 32, 48]

data = {benchmark: [] for benchmark in benchmarks}

for benchmark in benchmarks:
    ipc_values = []

    for pim_core in pim_cores:
        file_path = f"pim-{benchmark}-{pim_core}-threads.stats"
        ipc = extract_ipc(file_path)

        if ipc is not None:
            ipc_values.append(ipc)

    data[benchmark] = ipc_values

# Plot the data with a densening blue spectrum
bar_width = 0.15
bar_positions = np.arange(len(benchmarks))

norm = Normalize(vmin=min(pim_cores), vmax=max(pim_cores))
sm = ScalarMappable(cmap='Blues', norm=norm)
sm.set_array([])

for i, pim_core in enumerate(pim_cores):
    plt.bar(bar_positions + i * bar_width, [data[benchmark][i] for benchmark in benchmarks], bar_width,
            label=f'{pim_core} Units', color=sm.to_rgba(pim_core))

plt.xlabel('Benchmarks')
plt.ylabel('IPC')
plt.title('IPC Performance for GPM Benchmarks and Varying NDP Units')
plt.xticks(bar_positions + (len(pim_cores) - 1) * bar_width / 2, benchmarks)
plt.legend(title='Number of NDP Units')
plt.tight_layout()

plt.savefig('ipc_performance_plot.pdf')

