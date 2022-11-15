#%%
#from _typeshed import SupportsTrunc
import copy
import math

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

    # def __str__(self):
    #     return ' '.join([str(a) for a in [self.name, self.location, self.parent, self.f, self.sum_g]])


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


cities = initialize_all_cities()


def find_path(start_name, goal_name, search_mode):
    assert search_mode in ['a*', 'dijkstra']
    # initialize city instance variables, frontier and explored
    start_city = cities[start_name]
    goal_city = cities[goal_name]
    current_city = copy.deepcopy(start_city)
    current_city.sum_g = 0
    current_city.f = int(current_city.h(goal_city)) + current_city.sum_g if search_mode == 'a*'\
        else current_city.sum_g
    frontier = [current_city]
    explored = []
    # TODO: Expand node, update queues and reach goal city in this section
    while len(frontier) != 0:
        # Find node in frontier with smallest f
        dist = 10000
        current_city = frontier[0]
        for cty in frontier:
            if cty.f <= dist:
                dist = cty.f
                current_city = cty
        #if dist == 10000: return
        #print(city.name)
        
        if current_city.name == goal_name:
            #print('GOAL')
            #print('PARENT')
            #print(city.parent.name)
            break

        frontier.remove(current_city)
        explored.append(current_city)
        
        for neighbour in current_city.neighbours:
            dist = int(neighbour.h(goal_city)) + current_city.sum_g + current_city.g(neighbour) if search_mode == 'a*'\
                                    else current_city.sum_g + current_city.g(neighbour)
            
            if not(neighbour in explored) and not(neighbour in frontier):                
                neighbour.parent = current_city
                neighbour.sum_g = current_city.sum_g + current_city.g(neighbour)
                neighbour.f = dist
                frontier.append(neighbour)
            elif (neighbour in frontier) and (neighbour.f > dist):
                neighbour.parent = current_city
                neighbour.sum_g = current_city.sum_g + current_city.g(neighbour)
                neighbour.f = dist


    
    #print('PARENT')
    #print(city.parent.name)
    
    # TODO: return path from start to goal:
    path = []
    cost = current_city.sum_g
    #city = goal_city
    while current_city.parent != None:
        path.insert(0,current_city.name)
        current_city = current_city.parent
    path.insert(0,start_city.name)
    return (path, cost, explored)


#start_cities = ['Hamburg', 'Bremen', 'Lindau', 'Dresden', 'Stuttgart']
#goal_cities = ['Freiburg', 'Augsburg', 'Kiel', 'Karlsruhe', 'Stuttgart']
start_cities = ['Berlin', 'Stuttgart', 'Muenchen', 'Berlin', 'Kiel']
goal_cities = ['Hamburg', 'Frankfurt/Main', 'Nuernberg', 'Stuttgart', 'Garmisch-Part.']

for start, goal in zip(start_cities, goal_cities):
    for mode in ['a*']:#, 'dijkstra']:
        path, cost, explored = find_path(start, goal, mode)
        print(mode + ':')
        print(start, '-->', goal, ', Path:', path)
        print(start, '-->', goal, ', Cost:', cost)
        print(start, '-->', goal, ', Explored cities:', len(explored))
        print('\n')
    #print('\n' * 3)
#%%