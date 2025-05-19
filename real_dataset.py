import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

def get_high(result_file):
    data = pd.read_csv(result_file, index_col=0)
    num_high = data[(data['Completeness'].astype(float) > float(90)) & (data['Contamination'].astype(float) < float(0.05 * 100)) & data['pass.GUNC']].shape[0]
    return num_high

def plot_human():
    testing_list = ['CCMD98702133ST', 'CCMD45004878ST', 'CCMD38158721ST', 'CCMD53522274ST', 'CCMD72690923ST',
                    'CCMD22852639ST', 'CCMD95676152ST', 'CCMD41202658ST', 'CCMD23541216ST', 'CCMD76409700ST',
                    'CCMD65406197ST', 'CCMD32288175ST', 'CCMD59540613ST', 'CCMD42956136ST', 'CCMD75147712ST',
                    'CCMD35633353ST', 'CCMD53508245ST', 'CCMD46727384ST', 'CCMD76222476ST', 'CCMD31009081ST']
    training_num = [20,30,40,50,60,70,80,82]
    result_bowtie2 = 0
    for sample in testing_list:
        result_bowtie2 += get_high(f"real_datasets/human_gut/{sample}/bowtie2/result.csv")
    result_bowtie2_single = 0
    for sample in testing_list:
        result_bowtie2_single += get_high(f"real_datasets/human_gut/{sample}/bowtie2_single/result.csv")
    result_aemb = []
    for num in training_num:
        num_high = 0
        for sample in testing_list:
            num_high += get_high(f"real_datasets/human_gut/{sample}/{num}/result.csv")
        result_aemb.append(num_high)
    x_values = [20,30,40,50,60,70,80,90]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x_values , result_aemb , label='AEMB', color='#1b9e77',  width=4)
    ax.plot(x_values , [result_bowtie2] * 8, label='Bowtie2(multi)', color='#7570b3')
    ax.plot(x_values, [result_bowtie2_single] * 8, label='Bowtie2(single)', color='#e6ab02')

    ax.set_xlabel('Training samples used')
    ax.set_ylabel('Number of high-quality bins')
    ax.set_title('Human gut')
    ax.set_xticks(x_values)
    ax.set_ylim(200, max(result_aemb + [result_bowtie2]))
    ax.legend()

    fig.savefig('plots/Human_gut.pdf', dpi=300, bbox_inches='tight')

def plot_dog():
    testing_list = ['SAMN06172442','SAMN06172428', 'SAMN06172478', 'SAMN06172411', 'SAMN06172505','SAMN06172409', 'SAMN06172516', 'SAMN06172506','SAMN06172498',
                    'SAMN06172474', 'SAMN06172514', 'SAMN06172469', 'SAMN06172448', 'SAMN06172470', 'SAMN06172420', 'SAMN06172421', 'SAMN06172408',
                     'SAMN06172495', 'SAMN06172493', 'SAMN06172504']
    training_num = [20,30,40,50,60,70,80,90,100,110,120,129]
    result_bowtie2 = 0
    for sample in testing_list:
        result_bowtie2 += get_high(f"real_datasets/dog/{sample}/bowtie2/result.csv")
    print(result_bowtie2)
    result_bowtie2_single = 0
    for sample in testing_list:
        result_bowtie2_single += get_high(f"real_datasets/dog/{sample}/bowtie2_single/result.csv")
    print(result_bowtie2_single)
    result_aemb = []
    for num in training_num:
        num_high = 0
        for sample in testing_list:
            num_high += get_high(f"real_datasets/dog/{sample}/{num}/result.csv")
        result_aemb.append(num_high)
    print(result_aemb)

    x_values = [20,30,40,50,60,70,80,90,100,110,120,130]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x_values , result_aemb , label='AEMB', color='#1b9e77',  width=4)
    ax.plot(x_values , [result_bowtie2] * 12, label='Bowtie2(multi)', color='#7570b3')
    ax.plot(x_values, [result_bowtie2_single] * 12, label='Bowtie2(single)', color='#e6ab02')

    ax.set_xlabel('Training samples used')
    ax.set_ylabel('Number of high-quality bins')
    ax.set_title('Dog gut')
    ax.set_xticks(x_values)
    ax.set_ylim(400, max(result_aemb + [result_bowtie2]))
    ax.legend()

    fig.savefig('plots/Dog.pdf', dpi=300, bbox_inches='tight')
    plt.close()

def plot_tara():
    testing_list = ['TARA_132_SRF_0.22-3', 'TARA_094_SRF_0.22-3', 'TARA_102_SRF_0.22-3', 'TARA_138_SRF_0.22-3', 'TARA_076_SRF_0.45-0.8',
                'TARA_004_SRF_0.22-1.6', 'TARA_068_SRF_0.22-0.45', 'TARA_076_SRF_0.22-3', 'TARA_031_SRF_lt-0.22', 'TARA_123_SRF_0.45-0.8',
                'TARA_150_SRF_0.22-3', 'TARA_072_SRF_lt-0.22', 'TARA_067_SRF_lt-0.22', 'TARA_125_SRF_0.22-0.45', 'TARA_066_SRF_lt-0.22',
                'TARA_034_SRF_0.22-1.6', 'TARA_133_SRF_0.22-3', 'TARA_070_SRF_lt-0.22', 'TARA_124_SRF_0.22-0.45', 'TARA_068_SRF_0.45-0.8']
    training_num = [20,30,40,50,60,70,80,90,100,109]
    result_bowtie2  = 0
    for sample in testing_list:
        result_bowtie2 += get_high(f"real_datasets/ocean/{sample}/bowtie2/result.csv")
    print(result_bowtie2)
    result_bowtie2_single = 0
    for sample in testing_list:
        result_bowtie2_single += get_high(f"real_datasets/ocean/{sample}/bowtie2_single/result.csv")
    print(result_bowtie2_single)
    result_aemb = []
    for num in training_num:
        num_high = 0
        for sample in testing_list:
            num_high += get_high(f"real_datasets/ocean/{sample}/{num}/result.csv")
        result_aemb.append(num_high)
    print(result_aemb)

    x_values = [20,30,40,50,60,70,80,90,100,110]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x_values , result_aemb , label='AEMB', color='#1b9e77',  width=4)
    ax.plot(x_values , [result_bowtie2] * 10, label='Bowtie2(multi)', color='#7570b3')
    ax.plot(x_values, [result_bowtie2_single] * 10, label='Bowtie2(single)', color='#e6ab02')

    ax.set_xlabel('Training samples used')
    ax.set_ylabel('Number of high-quality bins')
    ax.set_title('Ocean')
    ax.set_xticks(x_values)
    ax.legend()
    fig.savefig('plots/Ocean.pdf', dpi=300, bbox_inches='tight')

def plot_soil():
    testing_list = ['SAMN06266461', 'SAMN06264631', 'SAMN06267101', 'SAMN06266485', 'SAMN06267081',
                'SAMN06264385', 'SAMN06266477', 'SAMN06266454', 'SAMN07631258', 'SAMN06266487',
                'SAMN06264883', 'SAMN06264630', 'SAMN06267100', 'SAMN06266458', 'SAMN06267089',
                'SAMN06268059', 'SAMN06266387', 'SAMN05421922', 'SAMN06266481', 'SAMN06266483']
    training_num = [20,30,40,50,60,70,80,90,100,101]
    result_bowtie2  = 0
    for sample in testing_list:
        result_bowtie2 += get_high(f"real_datasets/soil/{sample}/bowtie2/result.csv")
    print(result_bowtie2)
    result_bowtie2_single = 0
    for sample in testing_list:
        result_bowtie2_single += get_high(f"real_datasets/soil/{sample}/bowtie2_single/result.csv")
    print(result_bowtie2_single)
    result_aemb = []
    for num in training_num:
        num_high = 0
        for sample in testing_list:
            num_high += get_high(f"real_datasets/soil/{sample}/{num}/result.csv")
        result_aemb.append(num_high)
    print(result_aemb)

    x_values = [20,30,40,50,60,70,80,90,100,110]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x_values , result_aemb , label='AEMB', color='#1b9e77',  width=4)
    ax.plot(x_values , [result_bowtie2] * 10, label='Bowtie2(multi)', color='#7570b3')
    ax.plot(x_values, [result_bowtie2_single] * 10, label='Bowtie2(single)', color='#e6ab02')
    ax.set_xlabel('Training samples used')
    ax.set_ylabel('Number of high-quality bins')
    ax.set_title('Soil')
    ax.set_xticks(x_values)
    ax.legend()
    fig.savefig('plots/Soil.pdf', dpi=300, bbox_inches='tight')


if __name__ == '__main__':
    plot_human()
    print('\n')
    plot_dog()
    print('\n')
    plot_tara()
    print('\n')
    plot_soil()
