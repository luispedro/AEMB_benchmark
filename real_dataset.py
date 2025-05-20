import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import seaborn as sns
from os import makedirs


IN2CM = 2.54

COLOR_AEMB = cm.Dark2.colors[0]
COLOR_BOWTIE2_SINGLE = cm.Dark2.colors[1]
COLOR_BOWTIE2_MULTI = cm.Dark2.colors[5]

makedirs('plots', exist_ok=True)

def nr_hq_mags(result_file):
    # `boolean` type supports NA (unlike `bool`)
    data = pd.read_csv(result_file,
                        index_col=0,
                        dtype={'Completeness': 'float64', 'Contamination': 'float64', 'pass.GUNC': 'boolean'})

    return data.eval('Completeness > 90.0 and Contamination < 5 & `pass.GUNC`', engine='python').sum()

def load_data(env):
    from glob import glob
    import pandas as pd
    data = []
    for f in glob(f"real_datasets/{env}/*/*/result.csv"):
        _,_,sample,method,_ = f.split('/')
        data.append((sample, method, nr_hq_mags(f)))
    data = pd.DataFrame(data, columns=['sample', 'method', 'hq_mags'])
    data.drop('sample', axis=1, inplace=True)
    result = data.groupby('method').sum().squeeze()
    result_bowtie2 = result['bowtie2']
    result_bowtie2_single = result['bowtie2_single']
    result.drop(['bowtie2', 'bowtie2_single'], axis=0, inplace=True)
    result.index = result.index.map(int)
    result.sort_index(inplace=True)
    return result, result_bowtie2, result_bowtie2_single

for env in ['human_gut', 'dog', 'ocean', 'soil']:
    result_aemb, result_bowtie2, result_bowtie2_single= load_data(env)
    fig, ax = plt.subplots(figsize=(10/IN2CM, 6/IN2CM))
    ax.plot(result_aemb.index, result_aemb, '-o', label='AEMB', color=COLOR_AEMB)
    ax.hlines(y=result_bowtie2, xmin=result_aemb.index[0], xmax=result_aemb.index[-1], label='Bowtie2(multi)', color=COLOR_BOWTIE2_MULTI)
    ax.hlines(y=result_bowtie2_single, xmin=result_aemb.index[0], xmax=result_aemb.index[-1], label='Bowtie2(single)', color=COLOR_BOWTIE2_SINGLE)
    ax.set_xlabel('Training samples used')
    ax.set_ylabel('Number of high-quality bins')
    ax.set_title(env)
    ax.legend()
    fig.tight_layout()
    sns.despine(fig, trim=True)
    fig.savefig(f'plots/{env}.pdf', dpi=300, bbox_inches='tight')


