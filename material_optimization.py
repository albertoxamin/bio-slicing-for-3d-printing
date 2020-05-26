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
        best_cc = []
        for c in hardcoded:
            temp = problem.slice_and_get_fit(c)
            if temp < best_human:
                best_human = temp
                best_cc = c
        problem.slice_and_get_fit(best_cc, f'best_human_{model}_material')
        with open('summaries/summary_material.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([model, 'human', best_human, best_human, 0, best_cc])
        algorithms = ['ga', 'eda', 'es']
        for algorithm in algorithms:
            final_pop = evolve(algorithm, problem, hardcoded, prng, model=model, appendix="_material")
            print(f'{algorithm} completed')
            stats = inspyred.ec.analysis.fitness_statistics(final_pop)
            final_pop.sort(reverse=True)
            best = final_pop[0]
            problem.slice_and_get_fit(best.candidate, f'best_{model}_{algorithm}_material')
            with open('summaries/summary_material.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([model, algorithm, best_human, best.fitness, 1 - best.fitness / best_human, best.candidate])
            generation_plot(open(f"summaries/stats_{model}_{algorithm}_material.csv", "r"), algorithm=f"{model}_{algorithm}_material")

if __name__ == '__main__':
    main(display=True)
