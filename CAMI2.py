import matplotlib.pyplot as plt
from collections import defaultdict
import os
import pandas as pd

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

env2indices = {
        'Skin': [1, 13, 14, 15, 16, 17, 18, 19, 20, 28],
        'Oral': [6, 7, 8, 13, 14, 15, 16, 17, 18, 19],
        'Airways': [4, 7, 8, 9, 10, 11, 12, 23, 26, 27],
        'Gastrointestinal': [0, 1, 2, 3, 4, 5, 9, 10, 11, 12],
        'Urogenital': [0, 2, 3, 5, 6, 21, 22, 24, 25]
        }


def get_result(env, data_index, amber_path,run_time):
    method2strain = defaultdict(set)
    method2species = defaultdict(set)
    method2genus = defaultdict(set)

    for ix in data_index:
        taxi = pd.read_csv(f'CAMI2_multi_against_multi/{env}/taxonomic_profile_{ix}.txt', sep='\t', skiprows=3, dtype={'@@TAXID': str, 'TAXPATH': str})
        taxi_genus = taxi[taxi['RANK'] == 'genus']['@@TAXID'].values.tolist()
        taxi_species = taxi[taxi['RANK'] == 'species'][
            '@@TAXID'].values.tolist()

        genome_path = os.path.join(f'{amber_path}/S{ix}/amber{run_time}','genome')
        for root, dirs, files in os.walk(genome_path, topdown=False):
            for name in dirs:
                method_path = os.path.join(root, name)
                metric = pd.read_csv(os.path.join(method_path, 'metrics_per_bin.tsv'), sep='\t')
                com_90_pur_95 = metric[
                    (metric['Completeness (bp)'].astype(float) > float(0.9)) & (
                            metric['Purity (bp)'].astype(float) >= float(0.95))]
                strains = com_90_pur_95['Most abundant genome'].values.tolist()
                method2strain[name].update(strains)

                for strain in strains:
                    if strain in taxi['_CAMI_GENOMEID'].values.tolist():
                        taxi_split = taxi[taxi['_CAMI_GENOMEID'] == strain]['TAXPATH'].values[0].split('|')
                        if taxi_split[-2] in taxi_species:
                            method2species[name].add(taxi_split[-2])
                        if taxi_split[-3] in taxi_genus:
                            method2genus[name].add(taxi_split[-3])
    result = {}
    for method in ['bowtie2', 'seed', 'seed_hash', 'bwa', 'strobealign','fairy']:
        result[method] = (len(method2strain[method]),
                            len(method2species[method]),
                            len(method2genus[method]),
                          )

    return result

def plot_multi_against_multi_hash():
    for env,data_index in env2indices.items():
        result = {}

        for run_time in range(5):
            result_run = get_result(env, data_index, f"CAMI2_multi_against_multi/{env}", run_time)
            result['seed'] = [a + b / 5 for a, b in zip(result['seed'], result_run['seed'])]
            result['seed_hash'] = [a + b / 5 for a, b in zip(result['seed_hash'], result_run['seed_hash'])]

        print(result['seed_hash'])
        print(result['seed'])

        line_width = 1
        fig,ax = plt.subplots(figsize=(4, 4))

        ax.plot(['genus', 'species', 'strain'],
                 result['seed_hash'][::-1], label='AEMB(hash)', color='#7570b3',
                 linewidth=line_width, marker='o', )

        plt.plot(['genus', 'species', 'strain'],
                 result['seed'][::-1], label='AEMB', color='#1b9e77',
                 linewidth=line_width, marker='o', )

        plt.legend()
        plt.title(f"{env}", fontsize=20, alpha=1.0, color='black')
        plt.savefig(f'cami2_short_reads_{env}_multi_against_multi_hash.pdf', dpi=300, bbox_inches='tight')

for env, data_index in env2indices.items():
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
    fig,ax = plt.subplots(figsize=(4, 4))

    ax.plot(['genus', 'species', 'strain'],
             result['strobealign'][::-1], label='strobealign', color='#e7298a',
             linewidth=line_width, marker='o', )

    ax.plot(['genus', 'species', 'strain'],
             result['bwa'][::-1], label='BWA', color='#e6ab02',
             linewidth=line_width, marker='o', )

    ax.plot(['genus', 'species', 'strain'],
             result['bowtie2'][::-1], label='Bowtie2', color='#7570b3',
             linewidth=line_width, marker='o', )

    ax.plot(['genus', 'species', 'strain'],
             result['seed'][::-1], label='AEMB', color='#1b9e77',
             linewidth=line_width, marker='o', )


    ax.plot(['genus', 'species', 'strain'],
             result['fairy'][::-1], label='fairy', color='#66a61e',
             linewidth=line_width, marker='o', )


    ax.legend()
    ax.set_title(f"{env}", fontsize=20, alpha=1.0, color='black')
    fig.savefig(f'plots/cami2_short_reads_{env}_multi_against_multi_all.pdf', dpi=300, bbox_inches='tight')

