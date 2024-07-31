import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

def process_results(log_file):
    with open(log_file) as fh:
        running_time = 0
        memory = 0
        for line in fh:
            if line.strip().startswith("Command exited with non-zero"):
                print('error')
                continue

            name, value = line.strip().split(": ")
            value = value.strip('"')

            if name == "Exit status":
                if int(value) != 0:
                    print('error')

            if name == "Elapsed (wall clock) time (h:mm:ss or m:ss)":
                if '.' in value:
                    value = value.split(":")
                    value[-1] = round(float(value[-1]))
                else:
                    value = value.split(":")

                if len(value) == 2:
                    seconds = int(value[0]) * 60 + int(value[1])
                elif len(value) == 3:
                    seconds = int(value[0]) * 3600 + int(value[1]) * 60 + int(value[2])
                else:
                    raise Exception("Unknown time format {}".format(value))
                value = seconds
                running_time = value

            if name == 'Maximum resident set size (kbytes)':
                memory = int(value)/1024
    return running_time, memory

def plot():
    method_list = ['Bowtie2', 'Bwa', 'Strobealign', 'AEMB']
    env_result = {'Skin': [], 'Oral': [],
                  'Airways': [], 'Gastrointestinal': [],
                  'Urogenital': []}
    env_list = ['Airways', 'Gastrointestinal', 'Oral',  'Skin','Urogenital',]
    for env in env_list:
        print(env)
        if env == 'Urogenital':
            num = 9
        else:
            num = 10
        for tool in ['bowtie2', 'bwa', 'strobealign']:
            running_time = 0
            running_time += process_results(f'running_time/{env}/{tool}/indexing.txt')[0]
            for i in range(num):
                running_time += process_results(f"running_time/{env}/{tool}/map{i+1}.txt")[0]
                running_time += process_results(f"running_time/{env}/{tool}/sort{i+1}.txt")[0]
                running_time += process_results(f"running_time/{env}/{tool}/tobam{i+1}.txt")[0]
                running_time += process_results(f"running_time/{env}/{tool}/cov{i+1}.txt")[0]
            # print(f"{tool}: {running_time / 60} mins")
            env_result[env].append(running_time / 60)

        running_time = 0
        running_time += process_results(f"running_time/{env}/seed/indexing.txt")[0]
        for i in range(num):
            running_time += process_results(f"running_time/{env}/seed/map{i+1}.txt")[0]
        env_result[env].append(running_time / 60)
        # print(f"seed: {running_time / 60} mins")
    print(env_result)

    method_list1 = ['Bowtie2', 'Bwa', 'strobealign']
    for index, method in enumerate(method_list1):
        print(method)

        time_reduce = []
        for env in env_list:
            print(env_result[env][index] - env_result[env][3])
            print((env_result[env][index] - env_result[env][3]) / env_result[env][index])
            # num += (env_result[env][index] - env_result[env][3]) / env_result[env][index]
            time_reduce.append((env_result[env][index] - env_result[env][3]) / env_result[env][index])
        print(np.min(time_reduce), np.max(time_reduce))


    subset = pd.DataFrame(np.array([env_result['Airways'],env_result['Gastrointestinal'], env_result['Oral'], env_result['Skin'], env_result['Urogenital']]),
                          columns = method_list, index=['Airways','Gastrointestinal', 'Oral', 'Skin', 'Urogenital'])
    print(subset)
    ax = subset.plot(kind='bar',color = ['#e7298a', '#e6ab02', '#7570b3', '#1b9e77'], figsize=(8,4))
    ax.set_xticklabels(labels=['Airways','Gastrointestinal', 'Oral', 'Skin', 'Urogenital'], fontsize=10,color = 'black',rotation = 360)
    ax.set_ylabel('Time (mins)', fontsize=15,color = 'black')
    plt.savefig(f'CAMI2_running_time.pdf', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    plot()