from abc import abstractmethod

class Filter:
    '''
    Filters AcousticEvents based on a specified FilterType.\n
    PROXIMITY: filters events based on spatial distance between individuals.\n
    TEMPORAL: filters events based on temporal overlap or proximity between events.\n
    Can be composed to apply multiple filter criteria sequentially.
    '''
    def __init__(self, threshold: float):
        self.threshold = threshold

    @abstractmethod
    def apply(self, events: list) -> list:
        '''
        Applies the filter to a list of AcousticEvents.\n
        Returns filtered list of events meeting the threshold criteria.
        '''
        return []
    
class ProximityFilter(Filter):
    '''
    Filters AcousticEvents based on spatial distance between individuals.\n
    Retains events where distance between individuals is within threshold.
    '''
    def apply(self, events: list) -> list:
        return []

class TemporalFilter(Filter):
    '''
    Filters AcousticEvents based on temporal overlap or proximity between events.\n
    Retains events where temporal distance between individuals is within threshold.
    '''
    def apply(self, events: list) -> list:
        return []