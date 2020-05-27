
import csv
import matplotlib.pyplot as plt

data = {
    'hammer.stl':[[],[],[]],
    'pole.stl':[[],[],[]],
    'pikachu.stl':[[],[],[]],
    'holder.stl':[[],[],[]]
}

with open('summaries/summary.csv', 'r') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV, None)
    for row in readCSV:
        if row[1] != 'human':
            data[row[0]][['ga', 'eda', 'es'].index(row[1])].append(float(row[4]) * 100)


for benchmark in data.keys():
    labels = ['GA', 'EDA', 'ES']
    fig, axes = plt.subplots()
    bplot1 = axes.boxplot(data[benchmark],
                            vert=True,
                            patch_artist=True,
                            labels=labels)
    axes.set_title(benchmark)

    colors = ['pink', 'lightblue', 'lightgreen']
    for patch, color in zip(bplot1['boxes'], colors):
        patch.set_facecolor(color)

    axes.yaxis.grid(True)
    axes.set_xlabel('Algorithm')
    axes.set_ylabel('Percentage of cost decrease')

    plt.savefig(f"summaries/{benchmark.replace('.stl','')}_improvement.png")