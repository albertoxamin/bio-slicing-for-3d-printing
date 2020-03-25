from inspyred import benchmarks
from inspyred.ec.emo import Pareto
from inspyred.ec.variators import mutator
from pylab import *
import copy
import subprocess
import re
import math
import numpy as np

added_hardcoded = False

class Slicing():

    slic3r_path = '/Applications/PrusaSlicer.app/Contents/MacOS/PrusaSlicer'
    stl_file = 'pikachu.stl'
    ini_file = '/Users/alberto/Library/Application Support/PrusaSlicer/print/Anet A8.ini'
    operation_cost = 150 * 0.0052 / 60  # electricity cost per minute
    material_cost = 14 / 300 / 1000  # 300mt ~ 1kg, cost per mm

    def generator(self, random, args):
        global added_hardcoded
        if not added_hardcoded:
            added_hardcoded = True
            return [0, 0, 0, 0.2]
        individual = [random.uniform(0, 360) for i in range(3)]
        individual.append(random.choice([0.12, 0.16, 0.2, 0.24, 0.28]))
        return individual

    def slice_candidate(self, candidate, name=""):
        slicing = subprocess.Popen([self.slic3r_path, self.stl_file, '--gcode', '--rotate', str(candidate[0]),
                                    '--rotate-x', str(candidate[1]), '--rotate-y', str(
            candidate[2]), '--layer-height', str(candidate[3]), '--align-xy', '0,0', '--load', self.ini_file,
            '-o', './gcodes/' + name + '.gcode'], stdout=subprocess.DEVNULL)
        slicing.wait()

    def slice_and_get_fit(self, cs, name=""):
        if name == "":
            name=str(id(cs))
        self.slice_candidate(cs, name)
        tail = subprocess.Popen(
            ['tail', '-n150', './gcodes/' + name + '.gcode'], stdout=subprocess.PIPE)
        sed = subprocess.Popen(
            ['sed', '-n', '-e', '/M84/,$p'], stdin=tail.stdout, stdout=subprocess.PIPE)
        score = subprocess.Popen(
            ['sed', '-e', '/avoid/,$d'], stdin=sed.stdout, stdout=subprocess.PIPE)
        score_str = str(score.communicate())
        filament_length = float(re.findall(r"[0-9]+\.[0-9]+", score_str)[0])
        printing_time_match = re.findall(
            r"(\d*)h{0,1} (\d+)m (\d+)s", score_str)[0]
        printing_time_match = np.array(printing_time_match)
        printing_time_match[printing_time_match == ''] = 0
        printing_time = int(printing_time_match[0]) * 60 + int(
            printing_time_match[1]) + int(printing_time_match[2]) / 60
        # return filament_length * self.material_cost + printing_time * self.operation_cost
        return filament_length

    def __init__(self, constrained=False):
        self.maximize = False
        self.constrained = constrained

    def evaluator(self, candidates, args):
        fitness = []
        for cs in candidates:
            try:
                fitness.append(self.slice_and_get_fit(cs))
            except:
                print(cs)
                fitness.append(math.inf)
        return fitness
