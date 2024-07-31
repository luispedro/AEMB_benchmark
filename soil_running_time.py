import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from CAMI2_running_time import process_results

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

def plot():
    srr_list = ['SRR3989440', 'SRR3989449', 'SRR3989454', 'SRR3989475', 'SRR5436853',
                'SRR5438034', 'SRR5438046', 'SRR5438132', 'SRR5438874', 'SRR5438876']
    method_list = ["N = 24", "N = 25", "N = 26", 'N = 27', 'N = 28', 'N = 29', 'N = 30', 'AEMB(hash)', 'AEMB(default)']
    time_list = []
    memory_list = []

    for index in [24, 25, 26,27,28,29,30]:
        print(index)
        running_time = 0
        running_time += process_results(f"running_time/soil/seed_N/{index}/indexing.txt")[0]
        index_running_time = process_results(f"running_time/soil/seed_N/{index}/indexing.txt")[0]
        memory_usage = process_results(f"running_time/soil/seed_N/{index}/indexing.txt")[1]
        for i in srr_list:
            running_time += process_results(f"running_time/soil/seed_N/{index}/map_{i}.txt")[0]
            memory = process_results(f"running_time/soil/seed_N/{index}/map_{i}.txt")[1]
            if memory > memory_usage:
                memory_usage = memory
        time_list.append((running_time - index_running_time * 10) / 60)
        memory_list.append(memory_usage)

    running_time = 0
    running_time += process_results(f"running_time/soil/seed_hash/indexing.txt")[0]
    index_running_time = process_results(f"running_time/soil/seed_hash/indexing.txt")[0]
    memory_usage = process_results(f"running_time/soil/seed_hash/indexing.txt")[1]
    for i in srr_list:
        running_time += process_results(f"running_time/soil/seed_hash/map_{i}.txt")[0]
        memory = process_results(f"running_time/soil/seed_hash/map_{i}.txt")[1]
        if memory > memory_usage:
            memory_usage = memory
    time_list.append((running_time - index_running_time * 10) / 60)
    memory_list.append(memory_usage)

    running_time = 0
    running_time += process_results(f"running_time/soil/seed/indexing.txt")[0]
    index_running_time = process_results(f"running_time/soil/seed/indexing.txt")[0]
    memory_usage = process_results(f"running_time/soil/seed/indexing.txt")[1]
    for i in srr_list:
        running_time += process_results(f"running_time/soil/seed/map_{i}.txt")[0]
        memory = process_results(f"running_time/soil/seed/map_{i}.txt")[1]
        if memory > memory_usage:
            memory_usage = memory
    time_list.append((running_time - index_running_time * 10) / 60)
    memory_list.append(memory_usage)

    print(time_list)
    print(memory_list)

    print((memory_list[-2] - memory_list[-1]) / memory_list[-2])

    print( (time_list[-1] - time_list[-2]) / 10 )

    colors = ['#80cdc1','#666666','#a6761d','#e6ab02','#66a61e','#e7298a', '#d95f02', '#7570b3', '#1b9e77']

    # 创建柱形图
    bars = plt.bar(method_list, time_list, color=colors)

    plt.legend(bars, method_list)
    # 添加标题和标签
    # plt.title('Bar Chart with Custom Colors')
    plt.xlabel('Methods')
    plt.ylabel('Running time (mins)')

    # 显示图形
    # plt.show()
    plt.savefig(f'soil_time.pdf', dpi=300, bbox_inches='tight')
    plt.close()

    bars = plt.bar(method_list, memory_list, color=colors)

    plt.legend(bars, method_list)
    # 添加标题和标签
    # plt.title('Bar Chart with Custom Colors')
    plt.xlabel('Methods')
    plt.ylabel('Peak memory usage (MB)')
    # plt.show()
    plt.savefig(f'soil_memory.pdf', dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    plot()



