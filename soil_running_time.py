import matplotlib.pyplot as plt
from matplotlib import cm
from parse_output import parse_time_output

srr_list = ['SRR3989440', 'SRR3989449', 'SRR3989454', 'SRR3989475', 'SRR5436853',
            'SRR5438034', 'SRR5438046', 'SRR5438132', 'SRR5438874', 'SRR5438876']

running_times = []
memory = []
method_names = []

for index in [24, 25, 26, 27, 28, 29, 30, 'hash', 'default']:
    if index == 'hash':
        basedir = "running_time/soil/seed_hash"
        method_names.append(f'AEMB(hash)')
    elif index == 'default':
        basedir = "running_time/soil/seed"
        method_names.append(f'AEMB(default)')
    else:
        basedir = f"running_time/soil/seed_N/{index}"
        method_names.append(f'N = {index}')
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
    memory.append(memory_usage)

fig, ax = plt.subplots()
bars = ax.bar(method_names, running_times, color=cm.Dark2.colors)

ax.legend(bars, method_names)
ax.set_xlabel('Methods')
ax.set_ylabel('Running time (mins)')

fig.savefig(f'soil_time.pdf', dpi=300, bbox_inches='tight')
fig,ax = plt.subplots()
bars = ax.bar(method_names, memory, color=cm.Dark2.colors)

ax.legend(bars, method_names)
ax.set_xlabel('Methods')
ax.set_ylabel('Peak memory usage (MB)')
fig.savefig(f'soil_memory.pdf', dpi=300, bbox_inches='tight')
