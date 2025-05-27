import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import rcParams
import seaborn as sns
from parse_output import parse_time_output
from os import makedirs

rcParams['svg.fonttype'] = 'none'  # Use text for fonts in SVG

makedirs('plots', exist_ok=True)

IN2CM = 2.54

srr_list = ['SRR3989440', 'SRR3989449', 'SRR3989454', 'SRR3989475', 'SRR5436853',
            'SRR5438034', 'SRR5438046', 'SRR5438132', 'SRR5438874', 'SRR5438876']

running_times = []
memory = []
method_names = []

for index in [24, 25, 26, 27, 28, 29, 30, 'hash']:
    if index == 'hash':
        basedir = "running_time/soil/seed_hash"
        method_names.append(f'AEMB(hash)')
    else:
        basedir = f"running_time/soil/seed_N/{index}"
        method_names.append(f'B = {index}')
        if index == 27:
            method_names[-1] += '*'
    time_out = parse_time_output(f"{basedir}/indexing.txt")
    index_running_time = time_out.running_time
    memory_usage = time_out.memory_usage
    total_running_time = index_running_time
    for i in srr_list:
        time_out = parse_time_output(f"{basedir}/map_{i}.txt")
        total_running_time += time_out.running_time
        if time_out.memory_usage > memory_usage:
            memory_usage = time_out.memory_usage
    running_times.append((total_running_time - index_running_time * 10) / 60)
    memory.append(memory_usage / 1024)  # Convert memory from MB to GB

fig, (ax_rt, ax_mem) = plt.subplots(1,2, figsize=(9/IN2CM, 7/IN2CM))

ax_rt.bar(method_names, running_times, color=cm.Dark2.colors[1], width=0.8, align='center')
ax_mem.bar(method_names, memory, color=cm.Dark2.colors[5], width=0.8, align='center')

ax_rt.set_xticks(range(len(method_names)))
ells = ax_rt.set_xticklabels(method_names, rotation=90, ha='center', fontsize=7, va='bottom')
ax_mem.set_xticks(range(len(method_names)))
ax_mem.set_xticklabels(method_names, rotation=90, ha='center', fontsize=7, va='bottom')
for x in ax_rt.get_xticklabels():
    x.set_y(0.1)
for x in ax_mem.get_xticklabels():
    x.set_y(0.1)
sns.despine(fig, trim=True)
fig.tight_layout()
ax_rt.set_ylabel('Running time (mins)', fontsize=9)
ax_mem.set_ylabel('Memory usage (peak, GB)', fontsize=9)
fig.savefig(f'plots/Fig_run_time_mem.svg', dpi=300, bbox_inches='tight')
