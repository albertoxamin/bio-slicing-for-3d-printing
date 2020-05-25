import inspyred
import numpy as np
import csv
import math

def generation_plot(file, errorbars=True, algorithm=None):
    import matplotlib.pyplot as plt
    import matplotlib.font_manager 
    import numpy as np
    
    generation = []
    psize = []
    worst = []
    best = []
    median = []
    average = []
    stdev = []
    reader = csv.reader(file)
    for row in reader:
        generation.append(int(row[0]))
        psize.append(int(row[1]))
        worst.append(float(row[2]))
        best.append(float(row[3]))
        median.append(float(row[4]))
        average.append(float(row[5]))
        stdev.append(float(row[6]))
    stderr = [s / math.sqrt(p) for s, p in zip(stdev, psize)]
    
    data = [average, median, best, worst]
    colors = ['black', 'blue', 'green', 'red']
    labels = ['average', 'median', 'best', 'worst']
    figure = plt.figure()
    if errorbars:
        plt.errorbar(generation, average, stderr, color=colors[0], label=labels[0])
    else:
        plt.plot(generation, average, color=colors[0], label=labels[0])
    for d, col, lab in zip(data[1:], colors[1:], labels[1:]):
        plt.plot(generation, d, color=col, label=lab)
    plt.fill_between(generation, data[2], data[3], color='#e6f2e6')
    plt.grid(True)
    ymin = min([min(d) for d in data])
    ymax = 2*ymin
    yrange = ymax - ymin
    plt.ylim((ymin - 0.1*yrange, ymax + 0.1*yrange))  
    prop = matplotlib.font_manager.FontProperties(size=8) 
    plt.legend(loc='upper left', prop=prop)    
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    if algorithm == None:
        plt.show()
    else:
        plt.savefig(f"summaries/stats_{algorithm}.png")
