'''
Spatial Temporal Random Interactions Simulator
'''
from random import randint
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import math

class TemporalTerritorySimulator:
    '''
    The Simulator class generates random acoustic events for a single Ovenbird 
    territory, focusing on temporal distribution. Each event has a start time 
    with a fixed duration of 3 seconds. The null assumption is that events occur 
    completely at random in time with no interaction effects between individuals. 
    The analysis tests P(observed events | completely random events) to determine
    whether observed acoustic events deviate significantly from 
    this null temporal distribution.
    '''
    def __init__(self, seed: int, radius: int, coors: tuple) -> None:
        self.x, self.y = coors # Tuple unpacking
        self.r = radius # The radius
        self.seed = seed # Choose a random seed for this simulator object
        self.dist = None # extended later, choose a probability distribution that lies on the ovenbird territory
    
    def generateRandomAcousticEvents(self, SamplingDistribution, n: int) -> list:
        '''
        Takes in a SamplingDistribution and number of samples n to draw from it.\n
        Returns a list of AcousticEvents with temporal coordinates (start, end).\n
        Each event has a fixed duration of 3 seconds: end = start + 3.\n
        The sampling distribution can be specified to test different null assumptions,\n
        defaulting to a uniform distribution over the recording window.
        '''
        #x = math.sqrt(np.random.uniform(0, 200, 1000))

        return []
        

    def __str__(self) -> str:
        return f'''The territory has radius {self.r} at ({self.x}, {self.y}) with simulation seed {self.seed}'''

if __name__ == "__main__":
    info = '''
            This program tests the null hypothesis that birds sing completely at random 
            with no interaction effects between individuals. Under the null, we would 
            expect a uniform temporal distribution of events. It is expected that the 
            real data deviates from this, providing evidence of structured vocal behavior 
            to analyze.
           '''
    print(f"{info}")
    rand_numbers = [TemporalTerritorySimulator(randint(0, 1000), randint(1, 10), (randint(0, 200), randint(0, 200))) for x in range(0, 10)]
    num_info = [str(rand_numbers[x]) for x in range(0, len(rand_numbers))]

    for info in num_info:
        print(info)
