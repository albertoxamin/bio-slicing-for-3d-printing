#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6
import os
import shutil
from random import Random
from time import time

import inspyred
import matplotlib.pyplot

from slicing import Slicing, slicing_mutation

algorithm = 'ga'

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
    problem = Slicing(stl_file='models/pole.stl')
    print("These are the default fitnesses without evolution, that equal to placing the object in the build plate and slicing it with basic rotations")
    print(f'[0, 0, 0, 0.2] has a cost of {problem.slice_and_get_fit( [0, 0, 0, 0.2, 0]):.3} €')
    print(f'[90, 0, 0, 0.2] has a cost of {problem.slice_and_get_fit([90, 0, 0, 0.2, 0]):.3} €')
    print(f'[0, 90, 0, 0.2] has a cost of {problem.slice_and_get_fit([0, 90, 0, 0.2, 0]):.3} €')
    print(f'[0, 0, 90, 0.2] has a cost of {problem.slice_and_get_fit([0, 0, 90, 0.2, 0]):.3} €')
    if algorithm == 'ga':
        ea = inspyred.ec.GA(prng)
        ea.terminator = [inspyred.ec.terminators.evaluation_termination, inspyred.ec.terminators.diversity_termination]
        ea.variator = [inspyred.ec.variators.blend_crossover, slicing_mutation]
        ea.observer = [inspyred.ec.observers.stats_observer, inspyred.ec.observers.file_observer]
        final_pop = ea.evolve(generator=problem.generator, evaluator=inspyred.ec.evaluators.parallel_evaluation_mp,
                            mp_evaluator=problem.evaluator, mp_num_cpu=4,
                            pop_size=30,
                            maximize=problem.maximize,
                            statistics_file=open("stats.csv", "w"),
                            individuals_file=open("inds.csv", "w"),
                            bounder=problem.bounder,
                            max_evaluations=1000,
                            num_elites=3)

    if display:
        best = min(final_pop)
        problem.slice_and_get_fit(best.candidate, 'best')
        stats = inspyred.ec.analysis.fitness_statistics(final_pop)
        print(f"Best: {stats['best']} Worst: {stats['worst']} Mean: {stats['mean']} Std: {stats['std']}")
    return ea


if __name__ == '__main__':
    main(display=True)
