import tkinter as tk
import random
import time
import matplotlib.pyplot as plt
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


POP_SIZE = 100
BITS = 20
BOUNDS = [[0, 10], [0, 20], [0, 30]]
Pm = 0.05
GENERATIONS = 100
Pc = 1
Cp = 4



def decode(bounds, bits, genes):
    real_chromosome = []
    for i in range(len(bounds)):
        integer = int("".join(char for char in genes[i]), 2)
        real_value = bounds[i][0] + (integer / (2**bits)) * (
            bounds[i][1] - bounds[i][0]
        )
        real_chromosome.append(real_value)
    return real_chromosome


def objective_function(t):
    x = t[0]
    y = t[1]
    z = t[2]

    Objective_max = x**2 +y**2 +z**2 + x*y +z*y +x*z/13 

    return Objective_max


def multiple_crossover(parent1, parent2, cp):
    if cp == 1:
        index = random.randint(1, BITS - 1)
        child1 = [parent1[i][:index] + parent2[i][index:] for i in range(len(parent1))]
        child2 = [parent2[i][:index] + parent1[i][index:] for i in range(len(parent1))]
        return Chromosome(child1), Chromosome(child2)

    cp = random.sample(range(1, BITS), cp)
    cp.sort()
    # faster than appending in an empty list
    child1 = [[None] * BITS for _ in range(len(parent1))]
    child2 = [[None] * BITS for _ in range(len(parent1))]
    for j in range(len(parent1)):
        sum = 0
        flag = False
        for i in range(BITS):

            if sum < len(cp) and i == cp[sum]:
                flag = not flag
                sum += 1

            if flag == True:
                child1[j][i] = parent1[j][i]
                child2[j][i] = parent2[j][i]
            else:
                child1[j][i] = parent2[j][i]
                child2[j][i] = parent1[j][i]
    return Chromosome(child1), Chromosome(child2)


class Chromosome:
    def __init__(self, genes: list, prob=0, qprob=0):
        self.genes = genes
        self.prob = prob
        self.qprob = qprob

        self.real_genes = decode(BOUNDS, BITS, self.genes)
        self.fitness = objective_function(self.real_genes)

    @classmethod
    def rand(cls):
        chrome = [
            ["0" if random.random() >= 0.5 else "1" for x in range(BITS)]
            for r in range(len(BOUNDS))
        ]
        return cls(chrome)

    def get_bin(self):
        s = ""
        for gene in self.genes:
            s += "".join(gene) + " "
        return s

    def __str__(self):
        s = ""
        t = self.real_genes

        s += f" x={t[0]}, y={t[1]}, z={t[2]}, prob={self.qprob}, fitness={self.fitness}"
        return s


class GeneticAlgorithm:
    def __init__(self, size=POP_SIZE):
        self.size = size
        self.population = []
        self.flag = False  # if true pop has negative values
        for i in range(size):
            self.population.append(Chromosome.rand())
            if not self.flag and self.population[i].fitness < 0:
                self.flag = True

    def misc(self):
        self.fitness_sum = 0
        self.qprob = 0
        pop = self.population

        if self.flag:  # scale fitness values
            min_fitness = pop[0].fitness
            for chromosome in pop:
                if chromosome.fitness < min_fitness:
                    min_fitness = chromosome.fitness

            for chromosome in pop:
                chromosome.fitness -= (
                    min_fitness - 10
                )  # -10 because fitness can't be zero
                self.fitness_sum += chromosome.fitness
            self.fitness_average = self.fitness_sum / len(pop)
        else:
            for chromosome in pop:
                self.fitness_sum += chromosome.fitness
        self.fitness_average = self.fitness_sum / len(pop)
        for chromosome in pop:
            chromosome.prob = chromosome.fitness / self.fitness_sum
            self.qprob += chromosome.prob
            chromosome.qprob += self.qprob
        

    def selection(self):
        t = []
        for _ in range(self.size):
            r = random.random()
            for chromosome in self.population:
                if r <= chromosome.qprob:
                    t.append(chromosome)
                    break
        self.population = t

    # TODO #6 multiple crossover points
    def crossover(self, crossover_rate, cp):
        pop = self.population
        newpop = list()
        for i in range(int(len(pop) / 2)):
            parent1 = pop[2 * i - 1].genes
            parent2 = pop[2 * i].genes
            if random.random() <= crossover_rate:
                child1, child2 = multiple_crossover(parent1, parent2, cp)
                newpop.extend([child1,child2])
                

            else:
                newpop.extend([pop[2 * i - 1],pop[2*i]])
                
        self.population = newpop

    def mutation(self, mutation_rate: float):
        pop = self.population
        offsprings = []
        for chromosome in pop:
            z = chromosome.genes
            if random.random() <= mutation_rate:
                dummy = []
                for i in range(3):
                    j = random.randint(0, BITS - 1)
                    if z[i][j] == "1":  # flip
                        z[i][j] = "0"
                    else:
                        z[i][j] = "1"
                    dummy.append(z[i])
                offsprings.append(Chromosome(dummy))
            else:
                offsprings.append(Chromosome(z))
        self.population = offsprings

    def __str__(self):
        s = ""
        for chrome in self.population:

            s += f"{chrome.real_genes} {chrome.get_bin()} fitness ={chrome.fitness}, probability = {chrome.qprob} \n"
        return s

    def best(self):
        best_chrom = self.population[0]
        for chromosome in self.population:
            if chromosome.fitness > best_chrom.fitness:
                best_chrom = chromosome
        return best_chrom

    def run(self):
        ga = GeneticAlgorithm(POP_SIZE)
        s = [i for i in range(GENERATIONS)]
        fitn = [] 
        avr = [] 
        for i in range(GENERATIONS):
    
            ga.misc()
            ga.selection()
            ga.crossover(Pc,Cp)
            ga.mutation(Pm)
            fitn.append(ga.best())
            avr.append(ga.fitness_average)
            plt.scatter(s[i],fitn[i].fitness,color='r',s=10)
            plt.scatter(s[i],avr[i],color='g',s=10)

        plt.show()




ga = GeneticAlgorithm(POP_SIZE)
ga.run()