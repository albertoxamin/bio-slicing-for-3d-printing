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
    print('optimizing material usage')

    with open('summaries/summary_material.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['model', 'algorithm','best_human', 'best_evolved', 'decrease', 'genome'])
    for model in models:
        problem = Slicing(stl_file=f'models/{model}', kw_cost=0, block_duplicates=True)
        best_human = 9999
        for c in hardcoded:
            best_human = min(best_human, problem.slice_and_get_fit(c))
        algorithms = ['ga', 'eda', 'es']
        for algorithm in algorithms:
            final_pop = evolve(algorithm, problem, hardcoded, prng)
            print(f'{algorithm} completed')
            stats = inspyred.ec.analysis.fitness_statistics(final_pop)
            problem.slice_and_get_fit(min(final_pop).candidate, f'best_{model}_{algorithm}_material')
            with open('summaries/summary_material.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([model, algorithm, best_human, stats['best'], 1 - stats['best'] / best_human, min(final_pop).candidate])

if __name__ == '__main__':
    main(display=True)
