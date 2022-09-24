# %%
from math import prod
from time import sleep
import pandas  as pd
import seaborn as sns
import numpy   as np
import matplotlib.pyplot as plt

# initialize the inertia, cognition and influence
INERTIA = -0.4
COGNITION = 2.55
INFLUENCE = 1.33

# create a dict with entry 'function' and all population values
# define the function f1
def f0(p):
    return sum([pow(x,2) for x in p])
func0 = {   
    "f" : f0,
    "POP_SIZE" : 25,
    "MIN" : -100,
    "MAX" : 100,
    "V_BOUND" : 2,
    "PRECISION" : 0.01,
    "DIMENSION" : 30
}
def f1(p):
    absolut = [abs(x) for x in p]
    return sum(absolut) + prod(absolut)
func1 = {   
    "f" : f1,
    "POP_SIZE" : 25,
    "MIN" : -10,
    "MAX" : 10,
    "V_BOUND" : 1,
    "PRECISION" : 0.01,
    "DIMENSION" : 30
}
def f2(p):
    result = 0
    for i in range(0, len(p)):
        sum = 0
        for j in range(0, i):
            sum +=  p[j]
        result += pow(sum,2 )
    return result

func2 = {   
    "f" : f1,
    "POP_SIZE" : 25,
    "MIN" : -100,
    "MAX" : 100,
    "V_BOUND" : 3,
    "PRECISION" : 0.02,
    "DIMENSION" : 30
}
functions = [func0, func1, func2]
#%%
def create_population(functions, index):
    MIN = functions[index]['MIN']
    MAX = functions[index]['MAX']
    DIMENSION = functions[index]['DIMENSION']
    V_BOUND = functions[index]['V_BOUND']
    POP_SIZE = functions[index]['POP_SIZE']

    # create a dataframe "partiles" with the columns 'pos', 'velocity', 'fitness', 'particleBestFitnessValue', 'particleBestFitnessPos' 
    # and the rows from 0 to POP_SIZE
    population = pd.DataFrame(columns=['pos', 'velocity', 'fitness', 'particleBestFitnessValue', 'particleBestFitnessPos'], index=range(0, POP_SIZE))
    for i in range(0, POP_SIZE):
        # initialize the dataframe with random values, pos and particleBestFitnessPos should be an array of size DIMENSION with values between MIN and MAX, rounded to PRECISION, velocity should be between PRECISION and PRECISION*10, fitness and particleBestFitnessValue should be INFINITY
        population['pos'][i] = np.random.uniform(MIN, MAX, DIMENSION).round(2)
        population['particleBestFitnessPos'][i] = [np.random.uniform(MIN, MAX, DIMENSION).round(2)]
        population['velocity'][i] = round(np.random.uniform(-V_BOUND, V_BOUND), 2)
        population['fitness'][i] = np.inf
        population['particleBestFitnessValue'][i] = [np.inf]
    print('created population')
    return population

# %%

#%%
# define the function run
def run(population, functions, index, fig):
    print('running...')
    MIN = functions[index]['MIN']
    MAX = functions[index]['MAX']
    DIMENSION = functions[index]['DIMENSION']
    V_BOUND = functions[index]['V_BOUND']
    POP_SIZE = functions[index]['POP_SIZE']
    PRECISION = functions[index]['PRECISION']
    f = functions[index]['f']

    GLOBAL_BEST_FITNESS_VALUE = np.inf
    GLOBAL_BEST_FITNESS_POS = np.random.uniform(MIN, MAX, DIMENSION).round(2)

    RUN = True
    iteration = 1
    while RUN:
        for i in range(0, POP_SIZE):
            #print('dimension: ', i)
            # update velocity
            #print(population['particleBestFitnessPos'][i])
            v = INERTIA * population['velocity'][i] + COGNITION * np.random.random() * (population['particleBestFitnessPos'][i][-1] - population['pos'][i]) + INFLUENCE * np.random.random() * (GLOBAL_BEST_FITNESS_POS - population['pos'][i]).round(2)
            # bound the velocity to -3 and 3
            for x in range(0, len(v)):
                if v[x] > V_BOUND:
                    v[x] = V_BOUND
                elif v[x] < -V_BOUND:
                    v[x] = -V_BOUND
            # set the velocity
            population['velocity'][i] = v
            # update position
            population['pos'][i] = np.minimum(MAX, np.maximum(MIN, population['pos'][i] + population['velocity'][i]).round(2))
            # update fitness if new position is better
            fitness = f(population['pos'][i])
            if fitness <= population['fitness'][i]:
                population['fitness'][i] = fitness
                population['particleBestFitnessValue'][i].append(fitness)
                population['particleBestFitnessPos'][i].append(population['pos'][i])
                #print('AFTER CHANGE')
                #print(population['particleBestFitnessPos'][i])
                # update global best if new position is better
                if population['fitness'][i] <= GLOBAL_BEST_FITNESS_VALUE:
                    GLOBAL_BEST_FITNESS_VALUE = fitness
                    GLOBAL_BEST_FITNESS_POS = population['pos'][i]
        #print(population.head())
        if iteration % 100 == 0:
            print(f'iteration {iteration} with fitness {GLOBAL_BEST_FITNESS_VALUE}')
        
        if DIMENSION == 2:
            plot2D(population, fig)
        elif DIMENSION == 3:
            plot3D(population, fig)
        # stop if global best is < 10
        if abs(GLOBAL_BEST_FITNESS_VALUE) <= PRECISION:
            print('stopped after ', iteration, ' iterations')
            print('fitness: ', GLOBAL_BEST_FITNESS_VALUE)
            RUN = False
        iteration += 1
    return

# plot the positions of the particles in the population to a scatterplot
def init_2D_plot(population):
    plt.ion()
    plt.axis([functions[index]['MIN'], functions[index]['MAX'], functions[index]['MIN'], functions[index]['MAX']])
    fig, ax = plt.subplots()
    x, y = population['pos'].apply(lambda x: x[0]), population['pos'].apply(lambda x: x[1])
    sc = ax.scatter(population['pos'].apply(lambda x: x[0]), population['pos'].apply(lambda x: x[1]))
    return fig, sc
def plot2D(population, fig):
    x, y = population['pos'].apply(lambda x: x[0]), population['pos'].apply(lambda x: x[1])
    sc.set_offsets(np.c_[x, y])
    fig.canvas.draw()
    fig.canvas.flush_events()

def init_3D_plot(population):
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    x, y, z = population['pos'].apply(lambda x: x[0]), population['pos'].apply(lambda x: x[1]), population['pos'].apply(lambda x: x[2])
    sc = ax.scatter(x, y, z)
    return fig, sc
def plot3D(population, fig):
    x, y, z = population['pos'].apply(lambda x: x[0]), population['pos'].apply(lambda x: x[1]), population['pos'].apply(lambda x: x[2])
    sc._offsets3d = (x, y, z)
    fig.canvas.draw()
    fig.canvas.flush_events()

#%%
if __name__ == "__main__":

    index = 2
    functions[index]['DIMENSION'] = 3

    population = create_population(functions, index)

    if functions[index]['DIMENSION'] == 2:
        fig, sc = init_2D_plot(population)
        plot2D(population, fig)
    elif functions[index]['DIMENSION'] == 3:
        fig, sc = init_3D_plot(population)
        plot3D(population, fig)

    print('starting...')
    run(population, functions, index, fig)
    sleep(5)
# %%
