# %%
from math import ceil, prod, sqrt
from time import sleep
import pandas  as pd
import seaborn as sns
import numpy   as np
import matplotlib.pyplot as plt

# initialize the inertia, cognition and influence
INERTIA = -0.6031
COGNITION = -0.6485
INFLUENCE = 2.6475

# create a dict with entry 'function' and all population values
# define the function f1
def f0(p):
    return sum([pow(x,2) for x in p])
func0 = {   
    "f" : f0,
    "POP_SIZE" : 95,
    "MIN" : -100,
    "MAX" : 100,
    "V_BOUND" : 1,
    "PRECISION" : 0.01,
    "DIMENSION" : 30
}
def f1(p):
    absolut = [abs(x) for x in p]
    return sum(absolut) + prod(absolut)
func1 = {   
    "f" : f1,
    "POP_SIZE" : 95,
    "MIN" : -10,
    "MAX" : 10,
    "V_BOUND" : 1,
    "PRECISION" : 0.05,
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
    "POP_SIZE" : 95,
    "MIN" : -100,
    "MAX" : 100,
    "V_BOUND" : 1,
    "PRECISION" : 0.01,
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
def run(population, functions, index, enable_plot, iterations=0):
    data = []
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
            #print('Global best pos: ', GLOBAL_BEST_FITNESS_POS)
        
        data.append([iteration, GLOBAL_BEST_FITNESS_VALUE])
        if enable_plot == 1:    
            if DIMENSION == 2:
                plot2D(population)
            elif DIMENSION == 3:
                plot3D(population)
            elif DIMENSION > 3 and iteration % 10 == 0:
                plot(population, DIMENSION, MAX)
            fig.suptitle('i=' + str(iteration) + ' | f=' + str(round(GLOBAL_BEST_FITNESS_VALUE, 2)), fontsize=30)
        # stop if global best is < 100
        if abs(GLOBAL_BEST_FITNESS_VALUE) <= PRECISION or iteration == iterations:
            print('stopped after ', iteration, ' iterations')
            print('fitness: ', GLOBAL_BEST_FITNESS_VALUE)
            RUN = False
        iteration += 1
    print('Global best pos: ', GLOBAL_BEST_FITNESS_POS)
    return data

#%%
def init_plot(population, DIMENSION, MAX):
    plt.ion()
    n = ceil(sqrt(functions[index]['DIMENSION']))
    fig, axs = plt.subplots(n, n, figsize=(7, 7))
    positions = pd.DataFrame(population['pos'].to_numpy().tolist())
    x = 0
    for i in range(0, n):
        for j in range(0, n):
            if x < DIMENSION:
                axs[i, j].hist(positions[x], density=True, bins=MAX, range=(-MAX, MAX))
                #set the y axis to 0 to 1
                axs[i, j].set_title(f'{x}')
            else:
                axs[i, j].axis('off')
            x += 1
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    return fig, axs
def plot(population, DIMENSION, MAX):
    
    n = ceil(sqrt(functions[index]['DIMENSION']))
    positions = pd.DataFrame(population['pos'].to_numpy().tolist())
    maxima = positions.abs().max()
    x = 0
    for i in range(0, n):
        for j in range(0, n):
            if x < DIMENSION:
                axs[i, j].cla()
                axs[i, j].hist(positions[x], density=True, bins=max(20, int(MAX/2)), range=(min(-(MAX)/10, -maxima[x]), max(MAX/10, maxima[x])))
            x += 1
    fig.canvas.draw()
    fig.canvas.flush_events()
    return

# plot the positions of the particles in the population to a scatterplot
def init_2D_plot(population):
    plt.ion()
    fig, ax = plt.subplots()
    x, y = population['pos'].apply(lambda x: x[0]), population['pos'].apply(lambda x: x[1])
    plt.axis([functions[index]['MIN'], functions[index]['MAX'], functions[index]['MIN'], functions[index]['MAX']])
    sc = ax.scatter(population['pos'].apply(lambda x: x[0]), population['pos'].apply(lambda x: x[1]))
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    return fig, sc
def plot2D(population):
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
    mng = plt.get_current_fig_manager()
    sleep(0.5)
    mng.full_screen_toggle()
    return fig, sc
def plot3D(population):
    x, y, z = population['pos'].apply(lambda x: x[0]), population['pos'].apply(lambda x: x[1]), population['pos'].apply(lambda x: x[2])
    sc._offsets3d = (x, y, z)
    fig.canvas.draw()
    fig.canvas.flush_events()

#%%
if __name__ == "__main__":
    if int(input('Run analysis? (0,1)')) == 0:

        # get input from user for which function to run
        index = int(input('Enter the index of the function to run (0, 1, 2): '))
        # get input from user for the dimension of the function
        functions[index]['DIMENSION'] = int(input('Enter the dimension of the function: '))
        # get input from user for the number of particles
        functions[index]['POPULATION_SIZE'] = int(input('Enter the number of particles: '))
        # get input from user for the precision
        PRECISION = float(input('Enter the precision: '))
        enable_plot = int(input('Enable plot? (0,1): '))

        population = create_population(functions, index)

        if enable_plot == 1:
            if functions[index]['DIMENSION'] == 2:
                fig, sc = init_2D_plot(population)    
                plot2D(population)
            elif functions[index]['DIMENSION'] == 3:
                fig, sc = init_3D_plot(population)
                plot3D(population)
            else:
                fig, axs = init_plot(population, functions[index]['DIMENSION'], functions[index]['MAX'])
                plot(population, functions[index]['DIMENSION'], functions[index]['MAX'])
        sleep(0.2)
        print('starting...')

        run(population, functions, index, enable_plot)
        sleep(5)
    else:
        # analysis
        iterlim = 1000
        result = {}
        for i in range(len(functions)):
            print('function: ', i)
            population = create_population(functions, i)
            result[i] = run(population, functions, i, 0, iterlim)


        # %%
        for i in range(len(functions)):
            data = pd.DataFrame(result[i], columns=['iteration', 'fitness'])    
            # plot the fitness of the population over time
            plt.plot(data['iteration'], data['fitness'])
        # set y axis to log scale
        plt.yscale('log')
        plt.xlabel('iteration')
        plt.ylabel('fitness')
        # set title to the function name
        plt.title('Fitness of population over time')
        # create legend
        plt.legend([f'function {i}' for i in range(len(functions))])
        plt.ylim(0, 1000000)
        plt.xlim(0, 400)
        plt.show()
# %%
