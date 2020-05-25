from slicing import Slicing, slicing_mutation, hardcoded
import inspyred
import inspyred.ec.observers

def evolve(algorithm, problem, seeds, prng, model="", appendix=""):
    evolve_args = {
        'generator': problem.generator,
        'evaluator': inspyred.ec.evaluators.parallel_evaluation_mp,
        'mp_evaluator': problem.evaluator,
        'mp_num_cpu': 4,
        'pop_size': 30,
        'maximize': problem.maximize,
        'statistics_file': open(f"summaries/stats_{model}_{algorithm}{appendix}.csv", "w"),
        'individuals_file': open(f"summaries/inds_{model}_{algorithm}{appendix}.csv", "w"),
        'bounder': problem.bounder,
        'max_evaluations': 300,
        'seeds': seeds
    }
    if algorithm == 'ga':
        ea = inspyred.ec.GA(prng)
        ea.variator = [inspyred.ec.variators.uniform_crossover, slicing_mutation]
    elif algorithm == 'eda':
        ea = inspyred.ec.EDA(prng)
        ea.variator = [inspyred.ec.variators.uniform_crossover, slicing_mutation]
    elif algorithm == 'es':
        ea = inspyred.ec.ES(prng)
        ea.variator = [inspyred.ec.variators.uniform_crossover]
    if algorithm != 'none':
        ea.terminator = [inspyred.ec.terminators.evaluation_termination,
                        inspyred.ec.terminators.diversity_termination]
        ea.observer = inspyred.ec.observers.file_observer
        final_pop = ea.evolve(**evolve_args)
        return final_pop
