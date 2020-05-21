from slicing import Slicing, slicing_mutation, hardcoded
import inspyred
# import inspyred.ec.observers



def evolve(algorithm, problem, seeds, prng):
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
        'max_evaluations': 300,
        'seeds': seeds
    }
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
        final_pop = ea.evolve(**evolve_args)
        return final_pop
