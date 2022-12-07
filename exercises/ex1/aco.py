#%%
from time import sleep
import numpy as np
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

class AntColony():
    def __init__(self, distances, n_ants, n_iter, decay, alpha, beta, start, end):
        self.distances = distances
        self.pheromones = np.ones(distances.shape) * 0.000000000000000000000000000000001
        #wait = input("Press Enter to continue.")
        np.fill_diagonal(self.pheromones, 0)
        self.probabilities = np.zeros(distances.shape)

        self.start = start
        self.end = end
    
        self.n_ants = n_ants
        self.ants = []
        self.n_iter = n_iter

        self.decay = decay
        self.alpha = alpha
        self.beta = beta
    def init_probs(self):
        for i in range(self.distances.shape[0]):
            for j in range(self.distances.shape[1]):
                if i == j or self.distances[i, j] == 0:
                    continue
                self.probabilities[i, j] = 1.0 / (self.distances[i] > 0).sum()
    def update_probs(self):
        for i in range(self.distances.shape[0]):
            for j in range(self.distances.shape[1]):
                if i == j or self.distances[i, j] == 0:
                    continue
                
                self.probabilities[i, j] = ((self.pheromones[i, j] ** self.alpha) * ((1.0 / self.distances[i, j]) ** self.beta)
                                            / np.sum([(self.pheromones[i, k] ** self.alpha) * ((1.0 / self.distances[i, k]) ** self.beta) for k in range(self.distances.shape[0]) if k != i and self.distances[i, k] > 0]))
    def update_pheromones(self):
        self.pheromones *= self.decay

        count = 1
        for ant in self.ants:#sorted(self.ants, key=lambda ant: ant.distance):
            if ant.goal:
                for i in range(len(ant.path) - 1):
                    self.pheromones[ant.path[i], ant.path[i + 1]] += 1.0 / (ant.distance/100)
                    self.pheromones[ant.path[i + 1], ant.path[i]] += 1.0 / (ant.distance/100)
                count -= 1
        #print(self.pheromones.sum())
    def run(self):
        self.init_probs()
        for i in range(self.n_iter):
            self.ants = [Ant(self, self.start, self.end) for i in range(self.n_ants)]
            #print("Iteration: ", i)
            for ant in self.ants:
                if ant.finished:
                    continue
                ant.run()

            self.update_pheromones()
            if i % 20 == 0 or i<10:
                goal_ants = [ant for ant in self.ants if ant.path[-1] == ant.end]

                if goal_ants:
                    #print("{} / {} ants reached the goal".format(len(goal_ants), self.n_ants))
                    best_ant = min([a for a in self.ants if a.goal], key=lambda ant: ant.distance)
                    x = best_ant.distance
                    #print("I: {}, dist: {}".format(i, best_ant.distance))
                else:
                    #print("I: {}, dist: {}".format(i, np.inf))
                    x = np.inf
                plot(self.pheromones, i, x)

        goal_ants = [a for a in self.ants if a.goal]
        if goal_ants:
            best_ant = min(goal_ants, key=lambda ant: ant.distance)
            return best_ant.path, best_ant.distance
        else:
            return [], np.inf
class Ant():
    def __init__(self, colony, start=0, end=0):
        self.colony = colony
        self.start = start
        self.end = end
        self.path = [self.start]
        self.unvisited = list(range(len(self.colony.distances)))
        self.unvisited.remove(self.start)
        self.distance = 0
        self.finished = False
        self.goal = False
    def reset(self):
        self.path = [self.start]
        self.unvisited = list(range(len(self.colony.distances)))
        self.unvisited.remove(self.start)
        self.distance = 0
        self.finished = False
        self.goal = False
    def move(self):
        if not [x for x in self.unvisited if self.colony.distances[self.path[-1], x] > 0] or not self.unvisited:
            #print('Ant stuck at node {}'.format(self.path[-1]))
            self.finished = True
            return False

        probs = (colony.pheromones[self.path[-1]][self.unvisited] ** colony.alpha) * (colony.distances[self.path[-1]][self.unvisited] ** colony.beta) / np.sum((colony.pheromones[self.path[-1]][self.unvisited] ** colony.alpha) * (colony.distances[self.path[-1]][self.unvisited] ** colony.beta))
        probs = probs / probs.sum()
        
        next_node = np.random.choice(self.unvisited, p=probs)
        run = True
        
            
        self.path.append(next_node)
        self.unvisited.remove(next_node)
        #print('Ant moved to node {}'.format(next_node))
        if next_node == self.end:
            self.finished = True
            self.goal = True
        return True

    def run(self):
        while self.finished == False:
            self.move()
        self.distance = self.colony.distances[self.path[:-1], self.path[1:]].sum()

class DefineCity:
    def __init__(self, location, name, neighbours=[], dist_neighbours=[], parent=None, f=10000, sum_g=0):
        self.neighbours = neighbours
        self.location = location
        self.dist_neighbours = dist_neighbours
        self.parent = parent
        self.name = name
        self.f = f
        self.sum_g = sum_g
        assert len(self.dist_neighbours) == len(self.neighbours)

    def g(self, city):
        idx = self.neighbours.index(city)
        dist = self.dist_neighbours[idx]
        return dist

    def h(self, city2):
        source = self.location
        destination = city2.location
        lat_diff = source[0]-destination[0]
        long_diff = source[1]-destination[1]
        dist = math.sqrt(pow(lat_diff,2)+pow(long_diff,2))
        return dist
def initialize_all_cities():
    city = {}
    city['Aachen'] = DefineCity(location=[-209.60379, 249.47157], name='Aachen')
    city['Augsburg'] = DefineCity(location=[134.80635, -18.575178], name='Augsburg')
    city['Bayreuth'] = DefineCity(location=[179.32399, 157.053], name='Bayreuth')
    city['Berlin'] = DefineCity(location=[293.09943, 442.5178], name='Berlin')
    city['Bremen'] = DefineCity(location=[-16.931591, 504.64734], name='Bremen')
    city['Cottbus'] = DefineCity(location=[361.43076, 358.53146], name='Cottbus')
    city['Chemnitz'] = DefineCity(location=[269.5081, 254.68588], name='Chemnitz')
    city['Dresden'] = DefineCity(location=[325.56674, 279.0941], name='Dresden')
    city['Erfurt'] = DefineCity(location=[136.25624, 271.9933], name='Erfurt')
    city['Essen'] = DefineCity(location=[-141.96866, 325.35834], name='Essen')
    city['Frankfurt/Main'] = DefineCity(location=[-27.608, 175.58119], name='Frankfurt/Main')
    city['Frankfurt/Oder'] = DefineCity(location=[371.03522, 422.43652], name='Frankfurt/Oder')
    city['Freiburg'] = DefineCity(location=[-90.64952, -59.292046], name='Freiburg')
    city['Fulda'] = DefineCity(location=[43.13819, 223.62091], name='Fulda')
    city['Garmisch-Part.'] = DefineCity(location=[152.07657, -114.76524], name='Garmisch-Part.')
    city['Hamburg'] = DefineCity(location=[63.380383, 558.3458], name='Hamburg')
    city['Hannover'] = DefineCity(location=[44.825264, 426.9851], name='Hannover')
    city['Karlsruhe'] = DefineCity(location=[-48.82897, 53.54009], name='Karlsruhe')
    city['Kassel'] = DefineCity(location=[29.742897, 308.71664], name='Kassel')
    city['Kiel'] = DefineCity(location=[68.695816, 643.33014], name='Kiel')
    city['Koblenz'] = DefineCity(location=[-104.14378, 201.43147], name='Koblenz')
    city['Koeln'] = DefineCity(location=[-148.25447, 267.99976], name='Koeln')
    city['Leipzig'] = DefineCity(location=[229.1317, 311.15707], name='Leipzig')
    city['Lindau'] = DefineCity(location=[45.822735, -109.21826], name='Lindau')
    city['Magdeburg'] = DefineCity(location=[173.56235, 398.0283], name='Magdeburg')
    city['Mannheim'] = DefineCity(location=[-43.54089, 105.24141], name='Mannheim')
    city['Muenchen'] = DefineCity(location=[184.8133, -44.536476], name='Muenchen')
    city['Muenster'] = DefineCity(location=[-98.30054, 380.8315], name='Muenster')
    city['Neubrandenburg'] = DefineCity(location=[276.2144, 557.0144], name='Neubrandenburg')
    city['Nuernberg'] = DefineCity(location=[145.11511, 101.5798], name='Nuernberg')
    city['Osnabrueck'] = DefineCity(location=[-69.30297, 415.89078], name='Osnabrueck')
    city['Passau'] = DefineCity(location=[322.74014, 3.6142504], name='Passau')
    city['Regensburg'] = DefineCity(location=[220.39214, 53.54009], name='Regensburg')
    city['Rostock'] = DefineCity(location=[198.72835, 616.2598], name='Rostock')
    city['Saarbruecken'] = DefineCity(location=[-150.04137, 77.505005], name='Saarbruecken')
    city['Schwerin'] = DefineCity(location=[154.01888, 565.11285], name='Schwerin')
    city['Stuttgart'] = DefineCity(location=[8.18225, 27.57841], name='Stuttgart')
    city['Trier'] = DefineCity(location=[-173.55475, 134.86357], name='Trier')
    city['Ulm'] = DefineCity(location=[67.17258, -14.913567], name='Ulm')
    city['Wilhelmshaven'] = DefineCity(location=[-62.93731, 552.79846], name='Wilhelmshaven')
    city['Wuerzburg'] = DefineCity(location=[61.723507, 140.4113], name='Wuerzburg')

    city['Aachen'].neighbours = [city['Essen'], city['Koblenz'], city['Koeln']]
    city['Aachen'].dist_neighbours = [123, 145, 65]
    city['Augsburg'].neighbours = [city['Garmisch-Part.'], city['Muenchen'], city['Stuttgart'], city['Ulm']]
    city['Augsburg'].dist_neighbours = [117, 81, 149, 83]
    city['Bayreuth'].neighbours = [city['Nuernberg'], city['Wuerzburg']]
    city['Bayreuth'].dist_neighbours = [74, 147]
    city['Berlin'].neighbours = [city['Cottbus'], city['Frankfurt/Oder'], city['Magdeburg'], city['Neubrandenburg']]
    city['Berlin'].dist_neighbours = [125, 91, 131, 130]
    city['Bremen'].neighbours = [city['Hamburg'], city['Hannover'], city['Osnabrueck'], city['Wilhelmshaven']]
    city['Bremen'].dist_neighbours = [110, 118, 120, 110]
    city['Cottbus'].neighbours = [city['Berlin'], city['Dresden'], city['Frankfurt/Oder']]
    city['Cottbus'].dist_neighbours = [125, 138, 119]
    city['Chemnitz'].neighbours = [city['Erfurt'], city['Leipzig']]
    city['Chemnitz'].dist_neighbours = [160, 90]
    city['Dresden'].neighbours = [city['Cottbus'], city['Leipzig']]
    city['Dresden'].dist_neighbours = [138, 140]
    city['Erfurt'].neighbours = [city['Kassel'], city['Chemnitz']]
    city['Erfurt'].dist_neighbours = [135, 160]
    city['Essen'].neighbours = [city['Aachen'], city['Koeln'], city['Muenster'], city['Osnabrueck']]
    city['Essen'].dist_neighbours = [123, 75, 87, 135]
    city['Frankfurt/Main'].neighbours = [city['Fulda'], city['Karlsruhe'], city['Koblenz'], city['Mannheim'],
                                         city['Wuerzburg']]
    city['Frankfurt/Main'].dist_neighbours = [95, 135, 125, 106, 130]
    city['Frankfurt/Oder'].neighbours = [city['Berlin'], city['Cottbus']]
    city['Frankfurt/Oder'].dist_neighbours = [91, 119]
    city['Freiburg'].neighbours = [city['Karlsruhe']]
    city['Freiburg'].dist_neighbours = [130]
    city['Fulda'].neighbours = [city['Frankfurt/Main'], city['Kassel'], city['Wuerzburg']]
    city['Fulda'].dist_neighbours = [95, 105, 100]
    city['Garmisch-Part.'].neighbours = [city['Augsburg'], city['Muenchen']]
    city['Garmisch-Part.'].dist_neighbours = [117, 89]
    city['Hamburg'].neighbours = [city['Bremen'], city['Kiel'], city['Rostock'], city['Schwerin']]
    city['Hamburg'].dist_neighbours = [110, 90, 150, 120]
    city['Hannover'].neighbours = [city['Bremen'], city['Magdeburg'], city['Osnabrueck']]
    city['Hannover'].dist_neighbours = [118, 136, 135]
    city['Karlsruhe'].neighbours = [city['Frankfurt/Main'], city['Freiburg'], city['Mannheim'], city['Stuttgart']]
    city['Karlsruhe'].dist_neighbours = [135, 130, 58, 81]
    city['Kassel'].neighbours = [city['Erfurt'], city['Fulda']]
    city['Kassel'].dist_neighbours = [135, 105]
    city['Kiel'].neighbours = [city['Hamburg'], city['Schwerin']]
    city['Kiel'].dist_neighbours = [90, 139]
    city['Koblenz'].neighbours = [city['Aachen'], city['Frankfurt/Main'], city['Koeln'], city['Mannheim'],
                                  city['Trier']]
    city['Koblenz'].dist_neighbours = [145, 125, 110, 145, 128]
    city['Koeln'].neighbours = [city['Aachen'], city['Essen'], city['Koblenz'], city['Muenster']]
    city['Koeln'].dist_neighbours = [65, 75, 110, 144]
    city['Leipzig'].neighbours = [city['Dresden'], city['Magdeburg'], city['Chemnitz']]
    city['Leipzig'].dist_neighbours = [140, 108, 90]
    city['Lindau'].neighbours = [city['Ulm']]
    city['Lindau'].dist_neighbours = [126]
    city['Magdeburg'].neighbours = [city['Berlin'], city['Hannover'], city['Leipzig']]
    city['Magdeburg'].dist_neighbours = [131, 136, 108]
    city['Mannheim'].neighbours = [city['Frankfurt/Main'], city['Karlsruhe'], city['Koblenz'], city['Saarbruecken'],
                                   city['Stuttgart'], city['Trier']]
    city['Mannheim'].dist_neighbours = [106, 58, 145, 117, 138, 146]
    city['Muenchen'].neighbours = [city['Augsburg'], city['Garmisch-Part.'], city['Regensburg'], city['Ulm']]
    city['Muenchen'].dist_neighbours = [81, 89, 106, 124]
    city['Muenster'].neighbours = [city['Essen'], city['Koeln'], city['Osnabrueck']]
    city['Muenster'].dist_neighbours = [87, 144, 60]
    city['Neubrandenburg'].neighbours = [city['Berlin'], city['Rostock']]
    city['Neubrandenburg'].dist_neighbours = [130, 103]
    city['Nuernberg'].neighbours = [city['Bayreuth'], city['Regensburg'], city['Wuerzburg']]
    city['Nuernberg'].dist_neighbours = [74, 105, 108]
    city['Osnabrueck'].neighbours = [city['Bremen'], city['Essen'], city['Hannover'], city['Muenster']]
    city['Osnabrueck'].dist_neighbours = [120, 135, 135, 60]
    city['Passau'].neighbours = [city['Regensburg']]
    city['Passau'].dist_neighbours = [128]
    city['Regensburg'].neighbours = [city['Muenchen'], city['Nuernberg'], city['Passau']]
    city['Regensburg'].dist_neighbours = [106, 105, 128]
    city['Rostock'].neighbours = [city['Hamburg'], city['Neubrandenburg'], city['Schwerin']]
    city['Rostock'].dist_neighbours = [150, 103, 90]
    city['Saarbruecken'].neighbours = [city['Mannheim'], city['Trier']]
    city['Saarbruecken'].dist_neighbours = [117, 103]
    city['Schwerin'].neighbours = [city['Hamburg'], city['Kiel'], city['Rostock']]
    city['Schwerin'].dist_neighbours = [120, 139, 90]
    city['Stuttgart'].neighbours = [city['Augsburg'], city['Karlsruhe'], city['Mannheim'], city['Ulm']]
    city['Stuttgart'].dist_neighbours = [149, 81, 138, 100]
    city['Trier'].neighbours = [city['Koblenz'], city['Mannheim'], city['Saarbruecken']]
    city['Trier'].dist_neighbours = [128, 146, 103]
    city['Ulm'].neighbours = [city['Augsburg'], city['Lindau'], city['Muenchen'], city['Stuttgart']]
    city['Ulm'].dist_neighbours = [83, 126, 124, 100]
    city['Wilhelmshaven'].neighbours = [city['Bremen']]
    city['Wilhelmshaven'].dist_neighbours = [110]
    city['Wuerzburg'].neighbours = [city['Bayreuth'], city['Frankfurt/Main'], city['Fulda'], city['Nuernberg']]
    city['Wuerzburg'].dist_neighbours = [147, 130, 100, 108]
    return city
def initialize_city_distances(cities):
    # map all cities to numbers
    city_to_number = {}
    number_to_city = {}
    for i, city in enumerate(cities):
        city_to_number[city] = i
        number_to_city[i] = city
    # create a matrix of distances between all cities
    distances = np.zeros((len(cities), len(cities)))
    for city in cities.keys():
        for neighbour in cities[city].neighbours:
            distances[city_to_number[city], city_to_number[neighbour.name]] = cities[city].dist_neighbours[cities[city].neighbours.index(neighbour)]
    data = pd.DataFrame(distances)
    data.columns = [number_to_city[i] for i in range(len(cities))]
    data.index = [number_to_city[i] for i in range(len(cities))]
    return distances, city_to_number, number_to_city, data
def connectpoints(x,y,p1,p2, pheromone):
    x1, x2 = x[p1], x[p2]
    y1, y2 = y[p1], y[p2]
    plt.plot([x1,x2],[y1,y2],'o-', linewidth=min(pheromone[p1][p2]*8, 10), color='red')
    plt.plot([x1,x2],[y1,y2],'o-', linewidth=0.2, color='green')
def plot(pheromone, iteration, best):
    loc_dict = dict([(city, cities[city].location) for city in cities.keys()])

    plt.scatter([v[0] for k, v in loc_dict.items()], [v[1] for k, v in loc_dict.items()], color='black')
    # set x and y limits
    plt.xlim(-250, 400)
    plt.ylim(-150, 700)
    # change size of plot

    for k, v in loc_dict.items():
        plt.annotate(k, (v[0], v[1]))

    for idx, v in np.ndenumerate(distances):
        if v != 0:
            connectpoints([v[0] for k, v in loc_dict.items()], [v[1] for k, v in loc_dict.items()], idx[0], idx[1], pheromone)
    plt.title('Iteration {}, Pathcost: {}'.format(iteration, best))
    plt.show()
    plt.draw()
    # if input('save? y') == 'y':
    #     plt.savefig('handin/aco_i{}.png'.format(iteration))
    plt.pause(0.1)
    plt.clf()
#%%
if __name__ == '__main__':
    n_ants = 100
    n_iter = 50
    decay = 0.1
    alpha = 2
    beta = 1


    plt.ion()
    plt.figure(figsize=(6, 8), dpi=100)

    
    cities = initialize_all_cities()
    distances, c2n, n2c, pdData = initialize_city_distances(cities)


    # select wich city pairs to use
    start_cities =  ['Koeln',       'Kiel',             'Stuttgart',        'Muenchen', 'Berlin']
    goal_cities =   ['Hannover',    'Garmisch-Part.',   'Frankfurt/Main',   'Nuernberg','Hamburg']

    for start, goal in zip(start_cities, goal_cities):
        # Initialize Ant Colony
        print('Start: {}, Goal: {}'.format(start, goal))
        colony = AntColony(distances, n_ants, n_iter, decay, alpha, beta, start=c2n[start], end=c2n[goal])
        #colony = AntColony(distances, n_ants=3, n_iter=20, decay=0.6, alpha=0.8, beta=1, start=c2n[0], end=4)
        # Run Ant Colony
        path, cost = colony.run()
        # Print results
        #print('AntColony: Path = {}, Cost = {}'.format(path, cost))
        print(start, '-->', goal, ', Path:', [n2c[i] for i in path])
        print(start, '-->', goal, ', Cost:', cost)
        print('\n')
    
# %%
