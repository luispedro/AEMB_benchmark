import matplotlib.pyplot as plt
import os
import pandas as pd

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

skin_index = [1, 13, 14, 15, 16, 17, 18, 19, 20, 28]
oral_index = [6,7,8,13,14,15,16,17,18,19]
airways_index = [4,7,8,9,10,11,12,23,26,27]
gastrointestinal_index = [0, 1, 2, 3, 4, 5, 9, 10, 11, 12]
urogenital_index= [0, 2, 3, 5, 6, 21, 22, 24, 25]
env_list = ['Airways', 'Gastrointestinal', 'Oral', 'Skin','Urogenital']

def get_result(env, data_index, amber_path,run_time):
        genome_path = os.path.join(f'{amber_path}/S{data_index[0]}/amber0', 'genome')
        method_list = {}
        species_list = {}
        genus_list = {}

        for root, dirs, files in os.walk(genome_path, topdown=False):
            for name in dirs:
                method_list[name] = []
                species_list[name] = []
                genus_list[name] = []

        for temp in data_index:
            taxi = pd.read_csv(f'CAMI2_multi_against_multi/{env}/taxonomic_profile_{temp}.txt', sep='\t', skiprows=3, dtype={'@@TAXID': str, 'TAXPATH': str})
            taxi_genus = taxi[taxi['RANK'] == 'genus']['@@TAXID'].values.tolist()
            taxi_species = taxi[taxi['RANK'] == 'species'][
                '@@TAXID'].values.tolist()
            method_path_list = []
            genome_path = os.path.join(f'{amber_path}/S{temp}/amber{run_time}','genome')

            for root, dirs, files in os.walk(genome_path, topdown=False):
                for name in dirs:
                    method_path_list.append(os.path.join(root, name))

            for method_path in method_path_list:
                metric = pd.read_csv(os.path.join(method_path, 'metrics_per_bin.tsv'), sep='\t')
                com_90_pur_95 = metric[
                    (metric['Completeness (bp)'].astype(float) > float(0.9)) & (
                            metric['Purity (bp)'].astype(float) >= float(0.95))]
                strain_list = com_90_pur_95['Most abundant genome'].values.tolist()
                method_list[method_path.split('\\')[-1]].extend(strain_list)

                for temp_strain in strain_list:
                    if temp_strain in taxi['_CAMI_GENOMEID'].values.tolist():
                        taxi_split = taxi[taxi['_CAMI_GENOMEID'] == temp_strain]['TAXPATH'].values[0].split('|')
                        if taxi_split[-2] in taxi_species:
                            species_list[method_path.split('\\')[-1]].append(taxi_split[-2])
                        if taxi_split[-3] in taxi_genus:
                            genus_list[method_path.split('\\')[-1]].append(taxi_split[-3])
        result = {}
        for method in ['bowtie2', 'seed', 'seed_hash', 'bwa', 'strobealign','fairy']:
            result[method] = [len(list(set(method_list[method]))),len(list(set(species_list[method]))), len(list(set(genus_list[method])))]
        return result

def plot_multi_against_multi_hash():
    for env in env_list:
        print(env)
        if env == 'Skin':
            data_index = skin_index
        if env == 'Oral':
            data_index = oral_index
        if env == 'Airways':
            data_index = airways_index
        if env == 'Gastrointestinal':
            data_index = gastrointestinal_index
        if env == 'Urogenital':
            data_index = urogenital_index

        result = {'seed':[0,0,0], 'seed_hash':[0,0,0]}

        for run_time in range(5):
            result_run = get_result(env, data_index, f"CAMI2_multi_against_multi/{env}", run_time)
            result['seed'] = [a + b / 5 for a, b in zip(result['seed'], result_run['seed'])]
            result['seed_hash'] = [a + b / 5 for a, b in zip(result['seed_hash'], result_run['seed_hash'])]

        print(result['seed_hash'])
        print(result['seed'])

        line_width = 1
        plt.figure(figsize=(4, 4))

        plt.plot(['genus', 'species', 'strain'],
                 result['seed_hash'][::-1], label='AEMB(hash)', color='#7570b3',
                 linewidth=line_width, marker='o', )

        plt.plot(['genus', 'species', 'strain'],
                 result['seed'][::-1], label='AEMB', color='#1b9e77',
                 linewidth=line_width, marker='o', )

        plt.legend()
        plt.title(f"{env}", fontsize=20, alpha=1.0, color='black')
        plt.savefig(f'cami2_short_reads_{env}_multi_against_multi_hash.pdf', dpi=300, bbox_inches='tight')
        plt.close()

def plot_multi_against_multi_all():
    for env in env_list:
        print(env)
        if env == 'Skin':
            data_index = skin_index
        if env == 'Oral':
            data_index = oral_index
        if env == 'Airways':
            data_index = airways_index
        if env == 'Gastrointestinal':
            data_index = gastrointestinal_index
        if env == 'Urogenital':
            data_index = urogenital_index

        result = {'strobealign':[0,0,0],
                  'bwa':[0,0,0],
                  'bowtie2':[0,0,0],
                  'seed':[0,0,0],
                  'fairy':[0,0,0]}

        for run_time in range(5):
            result_run = get_result(env, data_index, f"CAMI2_multi_against_multi/{env}", run_time)
            result['strobealign'] = [a + b / 5 for a, b in zip(result['strobealign'], result_run['strobealign'])]
            result['bwa'] = [a + b / 5 for a, b in zip(result['bwa'], result_run['bwa'])]
            result['bowtie2'] = [a + b / 5 for a, b in zip(result['bowtie2'], result_run['bowtie2'])]
            result['seed'] = [a + b / 5 for a, b in zip(result['seed'], result_run['seed'])]
            result['fairy'] = [a + b / 5 for a, b in zip(result['fairy'], result_run['fairy'])]

        print(result['bwa'])
        print(result['strobealign'])
        print(result['bowtie2'])
        print(result['seed'])
        print(result['fairy'])

        line_width = 1
        plt.figure(figsize=(4, 4))

        plt.plot(['genus', 'species', 'strain'],
                 result['strobealign'][::-1], label='strobealign', color='#e7298a',
                 linewidth=line_width, marker='o', )

        plt.plot(['genus', 'species', 'strain'],
                 result['bwa'][::-1], label='BWA', color='#e6ab02',
                 linewidth=line_width, marker='o', )

        plt.plot(['genus', 'species', 'strain'],
                 result['bowtie2'][::-1], label='Bowtie2', color='#7570b3',
                 linewidth=line_width, marker='o', )

        plt.plot(['genus', 'species', 'strain'],
                 result['seed'][::-1], label='AEMB', color='#1b9e77',
                 linewidth=line_width, marker='o', )


        plt.plot(['genus', 'species', 'strain'],
                 result['fairy'][::-1], label='fairy', color='#66a61e',
                 linewidth=line_width, marker='o', )


        plt.legend()
        plt.title(f"{env}", fontsize=20, alpha=1.0, color='black')
        plt.savefig(f'cami2_short_reads_{env}_multi_against_multi_all.pdf', dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == '__main__':
    # plot_multi_against_multi_hash()
    plot_multi_against_multi_all()