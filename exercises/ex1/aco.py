from turtle import distance
import numpy as np
import pandas as pd

class AntColony():
    def __init__(self, distances, n_ants, n_iter, decay, alpha, beta):
        self.distances = distances
        self.pheromones = np.ones(distances.shape) / distances.size
        self.n_ants = n_ants
        self.n_iter = n_iter
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
    
class Ant():
    def __init__(self, colony):
        self.colony = colony
        self.tour = [0]
        self.unvisited = list(range(1, len(self.colony.distances)))
