"""
algorithm.py
The genetic algorithm engine.
04/2020 Kamil Zacharczuk
"""
import itertools
import random
from magazine import *

def performAlgorithm(magazine, boxes, populationSize, iterations, mutationProbability):
    if (not boxes): return []

    # Initial population is a set of populationSize random permutations of the boxes
    population = []
    while (len(population) < populationSize):
        perm = boxes[:] 
        random.shuffle(perm)
        population.append(perm)

    # Main algorithm loop
    for i in range(iterations):
        children = performCrossover(population)
        performMutation(children, mutationProbability)
        population = chooseNewPopulation(population, children, populationSize, magazine)

    return population[0]

def performCrossover(population):
    children = []
    genotype_len = len(population[0])
    for parents in list(itertools.combinations(population, 2)):
        ## Randomly choose two loci to split the genotype.
        # The locus means: split BEFORE the gene with this number.
        # First locus can be the position before any gene.
        # Second locus can be any position from locus_1 + 1 to AFTER the last gene.
        locus_1 = random.randint(0, genotype_len-1)
        locus_2 = random.randint(locus_1+1, genotype_len)

        twins = [[], []]
        boxes_missing_in_twin = [list(parents[0]), list(parents[1])] # Lists of boxes which didn't appear in the child yet.
        shift = 0
        for i in range(genotype_len):
            if (i < locus_1 or i >= locus_2): shift = 0
            else: shift = 1
            for j in range(2):
                box = parents[(j + shift) % 2][i]
                if (box in boxes_missing_in_twin[j]):
                    # This box hasn't appeared in this child yet - insert it into the child.
                    boxes_missing_in_twin[j].remove(box)
                    twins[j].append(box)
                else:
                    # This box has already appeared in the child - insert a box that has not.
                    twins[j].append(boxes_missing_in_twin[j].pop(0))
        assert (not boxes_missing_in_twin[0])
        assert (not boxes_missing_in_twin[1])
        for t in twins:
            children.append(t)

    return children

def performMutation(children, mutationProbability):
    mutationCount = 0
    rand_max = (int)(1/mutationProbability)
    print("Trying to mutate... ", end = '')
    for child in children:
        for i in range(len(child)):
            if (random.randint(1, rand_max) < 2):
                mutationCount += 1
                temp = child[i]
                child[i] = child[len(child)-1-i]
                child[len(child)-1-i] = temp

    print("Mutated ", str(mutationCount), " times among ", str(len(children)), " children.")


def chooseNewPopulation(population, children, populationSize, magazine):
    # Calculate fitness values for all genotypes 
    genotypesWithFitnessValues = pairGenotypesWithFitnessValues(population + children, magazine)
    # Sort genotypes descending by their fitness value
    genotypesWithFitnessValues.sort(key=lambda x: x[1], reverse=True)
    print("{:.6f}".format(genotypesWithFitnessValues[0][1]))
    # Get the list of the genotypes from the list of pairs
    unzipped = zip(*genotypesWithFitnessValues)
    new_population = list(list(unzipped)[0])
    # Truncate the new population to the populationSize size
    del new_population[populationSize:]
    
    return new_population

def pairGenotypesWithFitnessValues(population, magazine):
    result = []
    for p in population:
        for box in p:
            magazine.addBox(box)
        result.append((p, magazine.fill_factor))
        magazine.removeAllBoxes()

    return result


