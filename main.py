#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6
from random import Random
from time import time
import inspyred
import subprocess
from slicing import Slicing


def main(prng=None, display=False):
    if prng is None:
        prng = Random()
        prng.seed(time())
    subprocess.Popen(['rm', '-f', 'gcodes/*']).wait()
    problem = Slicing()
    print('No evolution individual with [0, 0, 0, 0.2] has a fitness of {0}'.format(
        problem.slice_and_get_fit([0, 0, 0, 0.2])))
    ea = inspyred.ec.GA(prng)
    ea.terminator = inspyred.ec.terminators.evaluation_termination
    final_pop = ea.evolve(generator=problem.generator, evaluator=inspyred.ec.evaluators.parallel_evaluation_mp,
                          mp_evaluator=problem.evaluator, mp_num_cpu=4,
                          pop_size=20,
                          maximize=problem.maximize,
                          bounder=inspyred.ec.Bounder(0, 360),
                          max_evaluations=200,
                          num_elites=1)
    if display:
        best = max(final_pop)
        problem.slice_candidate(best.candidate, 'best')
        print('Best Solution: \n{0}'.format(str(best)))
    return ea


if __name__ == '__main__':
    main(display=True)
