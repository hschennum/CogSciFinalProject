# Hayden Schennum
# 2025-11-21

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# df = pd.read_csv("param_results_full.txt", sep="\t")
# df['alpha'] = df['alpha'].round(1)
# data = df.pivot(index="beta", columns="alpha", values="time")


# plt.figure(figsize=(12, 6))
# plt.imshow(data, aspect='auto', cmap='viridis_r', origin='lower')
# plt.colorbar(label='Time to solve 1000 instances (s)')
# plt.xticks(ticks=np.arange(len(data.columns)), labels=data.columns)
# plt.yticks(ticks=np.arange(len(data.index)), labels=data.index)
# plt.xlabel('alpha')
# plt.ylabel('beta')
# plt.title('Solve Time vs alpha and beta')

# plt.savefig('factor_tuning.pdf', bbox_inches='tight')




algorithms = [
    "DFS + memoization", 
    "BFS: proximity heuristic", 
    "BFS: proximity and factor heuristic"
]
avg_T = [0.0056, 0.0045, 0.0022]
avg_F = [0.0114, 0.0128, 0.0082]
x = np.arange(len(algorithms))  # positions on x-axis
width = 0.2  # width of bars

fig, ax = plt.subplots(figsize=(8, 6))
bars_T = ax.bar(x - width/2, avg_T, width, label='T sets')
bars_F = ax.bar(x + width/2, avg_F, width, label='F sets')

# ax.grid(True)
ax.set_ylabel('Avg time per set (s)')
# ax.set_xlabel('Algorithm')
ax.set_title('Average Time per Set by Algorithm')
ax.set_xticks(x)
ax.set_xticklabels(algorithms)
ax.legend()
plt.savefig('TF_times.pdf', bbox_inches='tight')


