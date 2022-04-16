import random 
from numpy.random import rand, randint
import numpy as np 
bits = 20
bounds = [[0,10],[0,20],[0,30]]
pop_size = 50


def decoding(bounds, bits, chromosome):
    real_chromosome = list() 
    for i in range(len(bounds)):
        st, en = i * bits, (i*bits) + bits # extract chromosmo
        sub = chromosome[st:en] 
        chars = ''.join([str(s) for s in sub]) #convert to chart
        integer = int(chars,2)
        real_value = bounds[i][0] + (integer/(2**bits)) * (bounds[i][1] - bounds[i][0])
        real_chromosome.append(real_value) 
    return real_chromosome


pop = [randint(0,2,bits*len(bounds)).tolist() for _ in range(pop_size)]
#print(pop[1])
print(decoding(bounds,bits,pop[1]))

#print(bits*len(bounds))
#print(pop[0])

chromosome = randint(0,2,bits*len(bounds)).tolist()
print(chromosome)