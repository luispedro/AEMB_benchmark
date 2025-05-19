import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import numpy as np
from parse_output import parse_time_output as process_results
from collections import defaultdict

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

total_time = defaultdict(list)
envs = ['Airways', 'Gastrointestinal', 'Oral',  'Skin','Urogenital',]
for env in envs:
    print(env)
    for tool in ['bowtie2', 'bwa', 'strobealign', 'seed']:
        running_time = process_results(f'running_time/{env}/{tool}/indexing.txt').running_time
        for i in range(9 if env == 'Urogenital' else 10):
            running_time += process_results(f"running_time/{env}/{tool}/map{i+1}.txt").running_time
            if tool != 'seed':
                running_time += process_results(f"running_time/{env}/{tool}/sort{i+1}.txt").running_time
                running_time += process_results(f"running_time/{env}/{tool}/tobam{i+1}.txt").running_time
                running_time += process_results(f"running_time/{env}/{tool}/cov{i+1}.txt").running_time
        total_time[env].append(running_time / 60)

print(total_time)

for index, method in enumerate(['Bowtie2', 'Bwa', 'strobealign']):
    print(method)

    time_reduce = []
    for env in envs:
        print(total_time[env][index] - total_time[env][3])
        print((total_time[env][index] - total_time[env][3]) / total_time[env][index])
        # num += (total_time[env][index] - total_time[env][3]) / total_time[env][index]
        time_reduce.append((total_time[env][index] - total_time[env][3]) / total_time[env][index])
    print(np.min(time_reduce), np.max(time_reduce))


total_time = pd.DataFrame.from_dict(total_time, orient='index', columns=['Bowtie2', 'Bwa', 'Strobealign', 'AEMB']).sort_index()
print(total_time)
fig, ax = plt.subplots(figsize=(8,4))
colors = [cm.Dark2.colors[3], cm.Dark2.colors[5], cm.Dark2.colors[2], cm.Dark2.colors[3]]
total_time.plot(kind='bar', color=colors, ax=ax)
ax.set_xticklabels(labels=total_time.index, fontsize=10, color='black', rotation=360)
ax.set_ylabel('Time (mins)', fontsize=15, color='black')
fig.savefig(f'plots/CAMI2_running_time.pdf', dpi=300, bbox_inches='tight')

