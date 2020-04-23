from magazine import *
from algorithm import *
from magazine_gui import *
from solver import *

def main():
    default_population_size = 7
    default_iterations = 20
    default_mutation_probability = 1/300

    solver = Solver()
    gui = GUI(solver, default_population_size, default_iterations, default_mutation_probability)

    gui.displayGUI()

if __name__ == "__main__":
    main()

