import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import seaborn as sns
from parse_output import parse_time_output as process_results
from collections import defaultdict

total_time = defaultdict(list)
plt.rcParams['svg.fonttype'] = 'none'
IN2CM = 2.54

IS_HORIZONTAL = False


envs = ['Airways', 'Gastrointestinal', 'Oral',  'Skin','Urogenital',]
for env in envs:
    for tool in ['bowtie2', 'bwa', 'strobealign', 'seed']:
        running_time = process_results(f'running_time/{env}/{tool}/indexing.txt').running_time
        for i in range(9 if env == 'Urogenital' else 10):
            running_time += process_results(f"running_time/{env}/{tool}/map{i+1}.txt").running_time
            if tool != 'seed':
                running_time += process_results(f"running_time/{env}/{tool}/sort{i+1}.txt").running_time
                running_time += process_results(f"running_time/{env}/{tool}/tobam{i+1}.txt").running_time
                running_time += process_results(f"running_time/{env}/{tool}/cov{i+1}.txt").running_time
        total_time[env].append(running_time / 60)

total_time = pd.DataFrame.from_dict(total_time, orient='index', columns=['Bowtie2', 'Bwa', 'Strobealign', 'AEMB']).sort_index()

fig, ax = plt.subplots(figsize=(8/IN2CM,4))
colors = [cm.Dark2.colors[3], cm.Dark2.colors[5], cm.Dark2.colors[2], cm.Dark2.colors[0]]
data = pd.melt(total_time.reset_index(), id_vars='index', var_name='Method', value_name='Time (mins)')
if IS_HORIZONTAL:
    sns.barplot(data=data, hue='Method', y='index', x='Time (mins)', palette=colors, ax=ax, width=0.8, edgecolor='black', linewidth=0.5)
    ax.set_yticks(ticks=range(len(total_time.index)))
    ax.set_yticklabels(labels=total_time.index, fontsize=9, color='black', rotation=0)
    ax.set_xlabel('Time (mins)', fontsize=9, color='black')
    ax.set_ylabel(None)
else:
    sns.barplot(data=data, hue='Method', x='index', y='Time (mins)', palette=colors, ax=ax, width=0.8, edgecolor='black', linewidth=0.5)
    ax.set_xticks(ticks=range(len(total_time.index)))
    ax.set_xticklabels(labels=total_time.index, fontsize=9, color='black', rotation=0)
    ax.set_ylabel('Time (mins)', fontsize=9, color='black')
    ax.set_xlabel(None)

sns.despine(fig, trim=True)
fig.tight_layout()
fig.savefig(f'plots/CAMI2_running_time.svg', dpi=300, bbox_inches='tight')

