#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6
import os
import shutil
from random import Random
from time import time

import inspyred

import csv

from slicing import Slicing, hardcoded
from evolve import evolve
from justplot import generation_plot

folder = 'gcodes/'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)



def main(prng=None, display=False):
    if prng is None:
        prng = Random()
        prng.seed(time())

    models = os.listdir('models')
    nltr = '\n  '

    print(f"Available models:{nltr}{nltr.join([f'{i}) {x}' for i, x in enumerate(models)])}")

    with open('summaries/summary.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['model', 'algorithm','best_human', 'best_evolved', 'decrease', 'genome'])
    for model in models:
        problem = Slicing(stl_file=f'models/{model}')
        best_human = 9999
        for c in hardcoded:
            best_human = min(best_human, problem.slice_and_get_fit(c))
        algorithms = ['ga', 'eda', 'es']
        for algorithm in algorithms:
            for i in range(5):
                final_pop = evolve(algorithm, problem, hardcoded, prng, model=model, appendix=f"_{i}")
                print(f'{algorithm} run {i} completed')
                stats = inspyred.ec.analysis.fitness_statistics(final_pop)
                final_pop.sort(reverse=True)
                best = final_pop[0]
                problem.slice_and_get_fit(best.candidate, f'best_{model}_{algorithm}_{i}')
                with open('summaries/summary.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([model, algorithm, best_human, best.fitness, 1 - best.fitness / best_human, best.candidate])
                generation_plot(open(f"summaries/stats_{model}_{algorithm}_{i}.csv", "r"), algorithm=f"{model}_{algorithm}_{i}")


if __name__ == '__main__':
    main(display=True)
