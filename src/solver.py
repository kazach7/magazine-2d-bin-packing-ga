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

        winner = performAlgorithm(magazine, boxes, (int)(populationSize), (int)(iterations),
                                  (float)(mutationProbability))

        for box in winner:
            magazine.addBox(box)

        for x in range(mag_x):
            for y in range(mag_y):
                magazineShape[x][y] = magazine.getFieldState(x,y)

        return (magazineShape, magazine.fill_factor)