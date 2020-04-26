#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6
import os
import shutil
from random import Random
from time import time

import inspyred

import csv

from slicing import Slicing, hardcoded
from evolve import evolve

folder = 'gcodes/'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

def my_observer(population, num_generations, num_evaluations, args):
    best = max(population)
    # plt_gen.append(num_evaluations)
    # plt_best.append(best.fitness)
    args['fit'].append(best.fitness)
    # print('{0:6} -- {1} : {2}'.format(num_generations, 
                                    #   best.fitness, 
                                    #   str(best.candidate)))

def main(prng=None, display=False):
    if prng is None:
        prng = Random()
        prng.seed(time())

    models = os.listdir('models')
    nltr = '\n  '

    print(f"Available models:{nltr}{nltr.join([f'{i}) {x}' for i, x in enumerate(models)])}")

    with open('summary.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['model', 'algorithm','best_human','best_evolved', 'decrease'])
    for model in models:
        problem = Slicing(stl_file=f'models/{model}')
        # print("These are the default fitnesses without evolution, that equal to placing the object in the build plate and slicing it with basic rotations")
        best_human = 9999
        for c in hardcoded:
            # print(f'{c} has a cost of {problem.slice_and_get_fit(c):.3} €')
            best_human = min(best_human, problem.slice_and_get_fit(c))
        final_pops_fit = []
        algorithms = ['ga', 'eda']
        for algorithm in algorithms:
            best_fitnesses = []
            for i in range(5):
                final_pop = evolve(algorithm, problem, hardcoded, prng)
                print(f'{algorithm} run {i} completed')
                stats = inspyred.ec.analysis.fitness_statistics(final_pop)
                best_fitnesses.append(1 - stats['best'] / best_human)
                problem.slice_and_get_fit(min(final_pop).candidate, f'best_{model}_{algorithm}_{i}')
                with open('summary.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([model, algorithm, best_human, stats['best'], 1 - stats['best'] / best_human])
            # final_pops_fit.append(best_fitnesses)
            # if display:
            #     results.append()
                # best = min(final_pop)
                # problem.slice_and_get_fit(best.candidate, f'best')
                # stats = inspyred.ec.analysis.fitness_statistics(final_pop)
                # print(
                #     f"Best: {stats['best']} Worst: {stats['worst']} Mean: {stats['mean']} Std: {stats['std']}")
                # plt.plot(plt_gen, plt_best)
                # plt.show()
                # if 'n' not in input('Open best gcode? [Y/n]').lower():
                #     os.system('open ./gcodes/best.gcode')
        # fig = plt.figure('Best fitness obtained during 5 runs')
        # ax = fig.gca()
        # ax.boxplot(final_pops_fit)
        # ax.set_xticklabels(algorithms)
        # ax.set_xlabel('Algorithm')
        # ax.set_ylabel('Best fitness')
        # plt.show()
        # input('press to continue')


if __name__ == '__main__':
    main(display=True)
