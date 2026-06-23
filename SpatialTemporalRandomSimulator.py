'''
Spatial Temporal Random Interactions Simulator
'''
from random import randint

class SpacialTemporalRandomSimulator:
    '''
    The simulator class generates ovenbird territories and simulates the distribution of events \n
    For each simulation, there will be  \n
    It will be extended to include many other types of probability distributions for analyzing \n

    '''
    def __init__(self, seed: int, radius: int, coors: tuple) -> None:
        self.x, self.y = coors # Tuple unpacking
        self.r = radius # The radius
        self.seed = seed # Choose a random seed for this simulator object
    
    def __str__(self) -> str:
        return f'''The circle has radius {self.r} at ({self.x}, {self.y}) with simulation seed {self.seed}'''

if __name__ == "__main__":
    info = '''
            This program performs the null hypothesis: The birds sing randomly, and the events are spatially & temporally independent \n
            Essentially, we would be seeing a perfect cylinder for circular territories \n
            It is expected that this is not the case and that we would see some grooves and valleys, in which case we have something to work off \n
           '''
    print(f"{info}")
    rand_numbers = [SpacialTemporalRandomSimulator(randint(0, 1000), randint(1, 10), (randint(0, 200), randint(0, 200))) for x in range(0, 10)]
    num_info = [str(rand_numbers[x]) for x in range(0, len(rand_numbers))]

    for info in num_info:
        print(info)
