"""
main.py
Startup file of the 'Magazine' project.
Default algorithm parameters are set here.
04/2020 Kamil Zacharczuk
"""
from magazine import *
from algorithm import *
from gui import *
from solver import *

def main():
    default_population_size = 7
    default_iterations = 20
    default_mutation_probability = 1/30

    solver = Solver()
    gui = GUI(solver, default_population_size, default_iterations, default_mutation_probability)

    gui.displayGUI()

if __name__ == "__main__":
    main()

