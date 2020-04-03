#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6
import os
import shutil
from random import Random
from time import time

import inspyred
import matplotlib.pyplot

from slicing import Slicing, slicing_mutation, hardcoded

folder = 'gcodes/'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)


def main(prng=None, display=False):
    if prng is None:
        prng = Random()
        prng.seed(time())

    models = os.listdir('models')
    nltr = '\n  '
    print(
        f"Available models:{nltr}{nltr.join([f'{i}) {x}' for i, x in enumerate(models)])}")
    model = models[int(input('Choose the model to slice: '))]
    problem = Slicing(stl_file=f'models/{model}')
    print("These are the default fitnesses without evolution, that equal to placing the object in the build plate and slicing it with basic rotations")
    for c in hardcoded:
        print(f'{c} has a cost of {problem.slice_and_get_fit(c):.3} €')
    evolve_args = {
        'generator': problem.generator,
        'evaluator': inspyred.ec.evaluators.parallel_evaluation_mp,
        'mp_evaluator': problem.evaluator,
        'mp_num_cpu': 4,
        'pop_size': 30,
        'maximize': problem.maximize,
        'statistics_file': open("stats.csv", "w"),
        'individuals_file': open("inds.csv", "w"),
        'bounder': problem.bounder,
        'max_evaluations': 500,
        'seeds': hardcoded
    }
    algorithm = ''
    while algorithm not in ['ga', 'eda', 'none']:
        algorithm = input('Which algorithm do you want to use [ga|es|eda|none]: ').lower()
    if algorithm == 'ga':
        ea = inspyred.ec.GA(prng)
    elif algorithm == 'eda':
        ea = inspyred.ec.EDA(prng)
        evolve_args['num_selected'] = 3
        evolve_args['num_offspring'] = 30,
        evolve_args['num_elites'] = 3
    if algorithm != 'none':
        ea.terminator = [inspyred.ec.terminators.evaluation_termination,
                         inspyred.ec.terminators.diversity_termination]
        ea.variator = [
            inspyred.ec.variators.uniform_crossover, slicing_mutation]
        ea.observer = [inspyred.ec.observers.stats_observer,
                       inspyred.ec.observers.file_observer]
        final_pop = ea.evolve(**evolve_args)

    if display:
        best = min(final_pop)
        problem.slice_and_get_fit(best.candidate, f'best')
        stats = inspyred.ec.analysis.fitness_statistics(final_pop)
        print(
            f"Best: {stats['best']} Worst: {stats['worst']} Mean: {stats['mean']} Std: {stats['std']}")
        if 'n' not in input('Open best gcode? [Y/n]').lower():
            os.system('open ./gcodes/best.gcode')
    return ea


if __name__ == '__main__':
    main(display=True)
