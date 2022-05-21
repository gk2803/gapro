from operator import attrgetter
import tkinter as tk
import random
import time
import matplotlib.pyplot as plt
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot 
from matplotlib.animation import FuncAnimation
from itertools import count





class Chromosome:
    def __init__(self, genes: list,bounds, prob=0, qprob=0):
        self.bounds = bounds
        self.genes = genes
        self.prob = prob
        self.qprob = qprob

        self.real_genes = self.decode(self.genes)
        self.fitness = self.objective_function(self.real_genes)
  
    def decode(self,genes):
        real_chromosome = []
        for i in range(len(self.bounds)):
            integer = int("".join(char for char in genes[i]), 2)
            real_value = self.bounds[i][0] + (integer / (2**len(self.genes[0]))) * (
                self.bounds[i][1] - self.bounds[i][0]
            )
            real_chromosome.append(real_value)
        return real_chromosome

    @staticmethod
    def objective_function(t):
        x = t[0]
        y = t[1]
        z = t[2]
        Objective_max=x**3 + y**3 + z**4 + x*y*z
        #Objective_max = x**3-y**3-z**4+x*y*z 

        return Objective_max





class GeneticAlgorithm:
    def __init__(self, size, bits, bounds, pm, pc, cp ):
        self.size = size
        self.bits = bits
        self.bounds = bounds
        self.pm = pm 
        self.pc = pc
        self.cp = cp
        self.population = [Chromosome([[str(random.randint(0,1)) for _ in range(bits)] for _ in range(3)],self.bounds) for _ in range(self.size)]
    
            


    #calculates fitness scores/qprob
    def misc(self):
        self.fitness_sum = sum([chrome.fitness for chrome in self.population])
        self.fitness_average = self.fitness_sum / len(self.population)
        self.qprob=0
        for chromosome in self.population:
            chromosome.prob = chromosome.fitness / self.fitness_sum
            self.qprob += chromosome.prob 
            chromosome.qprob += self.qprob
         
    def roulette_selection(self):
        t = []
        for _ in range(self.size):
            r = random.random()
            for chromosome in self.population:
                if r <= chromosome.qprob:
                    t.append(chromosome)
                    break
        self.population = t

    def tournament_selection(self):
        selected = []
        for _ in range(self.size):
            selected.append(max(random.sample(self.population,2), key=attrgetter('fitness')))
        self.population = selected 

    def crossover(self):
        pop = self.population
        newpop = list()
        for i in range(int(len(pop) / 2)):
            parent1 = pop[2 * i - 1].genes
            parent2 = pop[2 * i].genes
            if random.random() <= self.pc:
                child1, child2 = self.multiple_crossover(parent1, parent2, self.cp)
                newpop.extend([Chromosome(child1,self.bounds),Chromosome(child2,self.bounds)])
                

            else:
                newpop.extend([pop[2 * i - 1],pop[2*i]])
                
        self.population = newpop

    def mutation(self):
        pop = self.population
        offsprings = []
        for chromosome in pop:
            z = chromosome.genes
            if random.random() <= self.pm:
                dummy = []
                for i in range(3):
                    j = random.randint(0, self.bits - 1)
                    if z[i][j] == "1":  # flip
                        z[i][j] = "0"
                    else:
                        z[i][j] = "1"
                    dummy.append(z[i])
                offsprings.append(Chromosome(dummy,self.bounds))
            else:
                offsprings.append(Chromosome(z,self.bounds))
        self.population = offsprings

    def __str__(self):
        s = ""
        for chrome in self.population:

            s += f"{chrome.real_genes} {chrome.get_bin()} fitness ={chrome.fitness}, probability = {chrome.qprob} \n"
        return s

    def best(self):
        return max(self.population,key=attrgetter('fitness'))



    @staticmethod
    def multiple_crossover(parent1, parent2, cp):
        bits = len(parent1[0])
        if cp == 1:
            index = random.randint(1, bits - 1)
            child1 = [parent1[i][:index] + parent2[i][index:] for i in range(len(parent1))]
            child2 = [parent2[i][:index] + parent1[i][index:] for i in range(len(parent1))]
            return child1, child2

        cp = random.sample(range(1, bits), cp)
        cp.sort()
        child1 = [[None] * bits for _ in range(len(parent1))]
        child2 = [[None] * bits for _ in range(len(parent1))]
        for j in range(len(parent1)):
            sum = 0
            flag = False
            for i in range(bits):

                if sum < len(cp) and i == cp[sum]:
                    flag = not flag
                    sum += 1

                if flag == True:
                    child1[j][i] = parent1[j][i]
                    child2[j][i] = parent2[j][i]
                else:
                    child1[j][i] = parent2[j][i]
                    child2[j][i] = parent1[j][i]
        return child1, child2

    def run(self):
        self.misc()
        self.tournament_selection()
        self.crossover()
        self.mutation()
        
        
    



#ga = GeneticAlgorithm(100,40,[[0, 10], [0, 20], [0, 30]],1,1,1)
#
#ga.run()
#print(ga.fitness_sum)
#
#for i in range(100):
#    ga.run()
#
#print(ga.fitness_average)