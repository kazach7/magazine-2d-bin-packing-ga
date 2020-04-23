##
# solver.py
# Object of this class takes the algorithm parameters and input data
# from the GUI, translates it to the form known by the algorithm engine,
# invokes the algorithm and translates its output for the GUI.
# 04/2020 Kamil Zacharczuk
##
from magazine import *
from algorithm import *

class Solver:
    def solve(self, magazineShape, boxesDimensions, populationSize, iterations, mutationProbability):
        mag_x = len(magazineShape)
        mag_y = len(magazineShape[0])
        magazine = Magazine(mag_x, mag_y)

        for x in range(mag_x):
            for y in range(mag_y):
                if (magazineShape[x][y] == "wall"):
                    magazine.setFieldStateToWall(x,y)

        boxes = []
        for b in boxesDimensions:
            boxes.append(Box(b[0], b[1]))

        # Run the algorithm.
        winner = performAlgorithm(magazine, boxes, (int)(populationSize), (int)(iterations),
                                  (float)(mutationProbability))

        # Check the fill factor for the winner solution.
        for box in winner:
            magazine.addBox(box)

        for x in range(mag_x):
            for y in range(mag_y):
                magazineShape[x][y] = magazine.getFieldState(x,y)

        return (magazineShape, magazine.fill_factor)