import math
import re
import subprocess
import time
import traceback

import inspyred
import numpy as np
from inspyred.ec.variators import mutator
from pylab import *

added_hardcoded = 0
hardcoded = [[0, 0, 0], [90, 0, 0], [0, 90, 0], [0, 0, 90]]
layer_heights = [0.12, 0.16, 0.2, 0.24, 0.28]
patterns = ['stars', 'concentric', 'honeycomb', '3dhoneycomb', 'gyroid', 'rectilinear',
            'grid', 'triangles', 'cubic', 'hilbertcurve', 'archimedeanchords', 'octagramspiral']


class SlicingBounder(object):
    def __call__(self, candidate, args):
        def closest(l, el): return min(l, key=lambda x: abs(x-el))
        for i, c in enumerate(candidate):
            if i < 3:
                candidate[i] = max(min(c, 360), 0)
            elif i == 3:
                candidate[i] = closest(layer_heights, c)
            elif i == 4:
                candidate[i] = round(c)
        return candidate


@mutator
def slicing_mutation(random, candidate, args):
    mut_rate = args.setdefault('mutation_rate', 0.1)
    bounder = args['_ec'].bounder
    mutant = candidate.copy()
    for i, m in enumerate(mutant):
        if random.random() < mut_rate:
            if i < 3:
                mutant[i] += random.gauss(0, (360) / 10.0)
            elif i == 3:
                mutant[i] = random.choice(layer_heights)
            elif i == 4:
                mutant[i] = random.randint(0, len(patterns) - 1)
    mutant = bounder(mutant, args)
    return mutant


class Slicing:

    def generator(self, random, args):
        global added_hardcoded
        individual = [random.uniform(0, 360) for i in range(3)]
        if added_hardcoded < len(hardcoded):
            individual = hardcoded[added_hardcoded]
            added_hardcoded = added_hardcoded + 1
        individual.append(random.choice(layer_heights))
        individual.append(random.randint(0, len(patterns) - 1))
        # an individual is an array of [rot_z, rot_x, rot_y, layer_height, infill_pattern]
        return individual

    def parse_gcode(self, gcode_str):
        filament_length = float(re.findall(r"[0-9]+\.[0-9]+", gcode_str)[0])
        printing_time_match = re.findall(
            r"(\d*)h{0,1} (\d+)m (\d+)s", gcode_str)
        if len(printing_time_match) == 0:  # printning time unavailable
            return math.inf
        printing_time_match = printing_time_match[0]
        printing_time_match = np.array(printing_time_match)
        printing_time_match[printing_time_match == ''] = 0
        printing_time = int(printing_time_match[0]) * 60 + int(
            printing_time_match[1]) + int(printing_time_match[2]) / 60
        return filament_length * self.material_cost + printing_time * self.operation_cost

    def slice_and_get_fit(self, cs, name=""):
        if name == "":
            name = str(id(cs))

        cat = f"cat gcodes/{name}.gcode | sed -n -e '/M84/,$p' | sed -e '/avoid/,$d'"
        candidate = f"--rotate {str(cs[0])} --rotate-x {str(cs[1])} --rotate-y {str(cs[2])} --layer-height {str(cs[3])} --fill-pattern {patterns[cs[4]]}"
        command = f"{self.slic3r_path} {self.stl_file} --gcode {candidate} --align-xy 0,0 --load '{self.ini_file}' -o ./gcodes/{name}.gcode && {cat}"
        try:
            output = subprocess.check_output(
                command, shell=True, executable='/bin/bash', universal_newlines=True, stderr=subprocess.DEVNULL)
            if len(re.findall(r"[0-9]+\.[0-9]+", output)) > 0 and len(re.findall(r"(\d*)h{0,1} (\d+)m (\d+)s", output)) > 0:
                return self.parse_gcode(output)
            else:
                print("File not found")
                return math.inf
        except subprocess.CalledProcessError as slicingException:
            print("Unprintable")
            return math.inf

    def __init__(self, constrained=False,
                 slic3r_path='/Applications/PrusaSlicer.app/Contents/MacOS/PrusaSlicer',
                 stl_file='models/pikachu.stl',
                 ini_file='/Users/alberto/Library/Application Support/PrusaSlicer/print/Anet A8.ini',
                 filament_kg_cost=14, kw_cost=0.052):
        self.maximize = False
        self.constrained = constrained
        self.bounder = SlicingBounder()
        self.slic3r_path = slic3r_path
        self.stl_file = stl_file
        self.ini_file = ini_file
        # electricity cost per minute, assuming a 150W printer
        self.operation_cost = 1.5 * kw_cost / 60
        self.material_cost = filament_kg_cost / 300 / 1000  # 300mt ~ 1kg, cost per mm

    def evaluator(self, candidates, args):
        fitness = []
        for cs in candidates:
            fitness.append(self.slice_and_get_fit(cs))
        return fitness
