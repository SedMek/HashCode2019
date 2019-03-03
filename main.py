import joblib as jb
from classes import *
import numpy as np
import random
import operator
import pandas as pd
import matplotlib.pyplot as plt
from random import shuffle
from itertools import islice
import input_output as io
import sys
import multiprocessing


class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    def routeDistance(self):
        if self.distance == 0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance

    def routeFitness(self):
        if self.fitness == 0:
            # +1 to avoid division by zero
            self.fitness = - 1 / float(1 + self.routeDistance())
        return self.fitness


def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route


def initialPopulation(popSize, cityList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))
    return population


def rankRoutes(population):
    fitnessResults = {}
    for i in range(0, len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)


def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()

    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i, 3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults


def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool


def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child


def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0, eliteSize):
        children.append(matingpool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children


def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))

            city1 = individual[swapped]
            city2 = individual[swapWith]

            individual[swapped] = city2
            individual[swapWith] = city1
    return individual


def mutatePopulation(population, mutationRate):
    mutatedPop = []

    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop


def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    print("Initial distance: " + str(1 / rankRoutes(pop)[0][1]))

    for i in range(0, generations):
        if (i % 10 == 0):
            print("-- iteration %d -- " % i)
        pop = nextGeneration(pop, eliteSize, mutationRate)

    print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute


def write_Slideshow_to_file(slideshow, output_name="sexybaby.txt"):
    with open(output_name, "w") as file:
        file.write("{}\n".format(len(slideshow.slides)))
        for slide in slideshow.slides:
            ID = slide.id
            if len(ID) == 1:
                file.write("{}\n".format(ID[0]))
            else:
                file.write("{} {}\n".format(ID[0], ID[1]))

# Create a set of slides following the rationale of the groupment by biggest tags


def get_horizontals_from_collection(collection, groupby="average", filename=""):

    # Create a set of vertical and horizontal pictures
    null_photo = Photo(orientation="", tags=[])
    collection_V = []
    collection_H = []

    for photo in collection:
        if photo.orientation == "V":
            collection_V.append(photo)
        else:
            collection_H.append(photo)

    # Sort pictures in place by number of tags
    collection_V.sort(key=lambda photo: len(photo.tags), reverse=True)
    collection_H.sort(key=lambda photo: len(photo.tags), reverse=True)

    # generate slides
    m = len(collection_V)
    slides_fromVerticals = []
    index = 0
    if groupby == "2by2":
        while index < m:
            slides_fromVerticals.append(
                Slide([collection_V[index], collection_V[index+1]]))
            index += 2
    else:
        if m % 2 == 1:
            collection_V = collection_V[1:]
        for i in range(m//2):
            slides_fromVerticals.append(
                Slide([collection_V[m - 1 - i], collection_V[i]]))

    slides_fromHorizontals = [Slide([photo]) for photo in collection_H]
    jb.dump(collection_V, "collection_V_{}.joblib".format(filename))
    jb.dump(collection_H, "collection_H_{}.joblib".format(filename))
    jb.dump(slides_fromVerticals,
            "slides_fromVerticals_{}_{}.joblib".format(groupby, filename))
    jb.dump(slides_fromHorizontals,
            "slides_fromHorizontals_{}.joblib".format(filename))
    return slides_fromVerticals, slides_fromHorizontals


def get_horizontals_from_file(filename, groupby="average"):
    return jb.load("slides_fromVerticals_{}_{}.joblib".format(groupby, filename)), jb.load("slides_fromHorizontals_{}.joblib".format(filename))


def get_batches(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def geneticAlgorithmMap(slides):
    return geneticAlgorithm(population=slides, popSize=100, eliteSize=20, mutationRate=0.01, generations=300)


if __name__ == "__main__":

    print("reading from:", sys.argv[-1])
    photos = io.read(sys.argv[-1])
    slides_fromVerticals, slides_fromHorizontals = get_horizontals_from_collection(
        photos, groupby="average")
    slides = slides_fromVerticals + slides_fromHorizontals
    slides_batches = list(get_batches(slides, 1000))

    num_proc = int(sys.argv[-2])
    pool = multiprocessing.Pool(num_proc)
    print("using %d processors out of %d" %
          (num_proc, multiprocessing.cpu_count()))

    results = []
    res_file = []

    for sld in slides_batches:
        results.append(pool.apply_async(geneticAlgorithmMap, [sld]))

    for result in results:
        res_file += result.get()

    sh = SlideShow(res_file, None)

    print("writing to", "output"+sys.argv[-1])
    write_Slideshow_to_file(sh, "output/"+sys.argv[-1])
