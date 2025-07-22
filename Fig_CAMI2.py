import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import os
import pandas as pd
from os import makedirs

makedirs('plots', exist_ok=True)

plt.rcParams['svg.fonttype'] = 'none' # Make sure text is not converted to paths in SVG (so they can be edited)
IN2CM = 2.54
LINE_WIDTH = 1

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



fig,axes = plt.subplots(1, len(env2indices), figsize=(17/IN2CM, 6/IN2CM), sharex=True)
fig_hash,axes_hash = plt.subplots(1, len(env2indices), figsize=(17/IN2CM, 6/IN2CM), sharex=True)

for ax, ax_hash, (env, data_index) in zip(axes.flat, axes_hash.flat, env2indices.items()):
    result = pd.DataFrame()
    for run_time in range(5):
        rt = get_result(env, data_index, f"CAMI2_multi_against_multi/{env}", run_time)
        result = result.add(pd.DataFrame.from_dict(rt, orient='index', columns=['strain', 'species', 'genus']), fill_value=0)
    # get the average over the 5 runs
    result /= 5



    order = ['genus', 'species', 'strain']
    tool2color = {
            'strobealign': '#e7298a',
            'bwa': '#e6ab02',
            'bowtie2': '#7570b3',
            'seed': '#1b9e77',
            'seed_hash': '#d95f02',
            'fairy': '#66a61e'
            }
    for tool in ['strobealign', 'bwa', 'bowtie2', 'seed', 'fairy']:
        ax.plot(order,
                result.loc[tool, order],
                label=tool, color=tool2color[tool],
                linewidth=LINE_WIDTH, marker='o', )


    for tool in ['seed_hash', 'seed']:
        ax_hash.plot(order,
                     result.loc[tool, order],
                     label=tool, color=tool2color[tool],
                     linewidth=LINE_WIDTH, marker='o', )

    for x in (ax, ax_hash):
        x.set_title(f"{env}", alpha=1.0, fontsize=9)
        x.set_xticks([0, 1, 2])
        x.set_xticklabels(order, rotation=90)

for f in (fig, fig_hash):
    sns.despine(f, trim=True)
    f.tight_layout()
ax.legend()
fig.savefig(f'plots/cami2_short_reads.svg', dpi=300, bbox_inches='tight')

ax_hash.legend()
fig_hash.savefig(f'plots/cami2_short_reads_multi_against_multi_hash.svg', dpi=300, bbox_inches='tight')
