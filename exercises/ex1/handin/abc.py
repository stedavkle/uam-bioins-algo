#%%
from time import sleep
import time
import pandas as pd
import numpy as np
from math import ceil, prod, sqrt, floor
import matplotlib.pyplot as plt
import seaborn as sns

def f0(p):
    return sum([pow(x,2) for x in p])
func0 = {   
    "f" : f0,
    "POP_SIZE" : 95,
    "MIN" : -100,
    "MAX" : 100,
    "V_BOUND" : 1,
    "PRECISION" : 0.1,
    "DIMENSION" : 30,
    "MAX_TRIALS" : 1000
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
    "PRECISION" : 0.1,
    "DIMENSION" : 30,
    "MAX_TRIALS" : 1000
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
    "PRECISION" : 0.1,
    "DIMENSION" : 30,
    "MAX_TRIALS" : 1000
}
functions = [func0, func1, func2]

#%%
def init(function_index):
    MIN = functions[function_index]['MIN']
    MAX = functions[function_index]['MAX']
    DIMENSION = functions[function_index]['DIMENSION']
    V_BOUND = functions[function_index]['V_BOUND']
    POP_SIZE = functions[function_index]['POP_SIZE']
    PRECISION = functions[function_index]['PRECISION']

    employed_count = ceil(POP_SIZE / 2)
    onlocker_count = POP_SIZE - employed_count

    bees = pd.DataFrame(np.random.uniform(MIN, MAX, (POP_SIZE, DIMENSION)).round(1))
    data = pd.DataFrame(bees.apply(lambda row: functions[function_index]['f'](row), axis=1), columns=['fitness'])
    data['trial'] = 0

    return bees, data
#%%
def employed_bee_phase(bees, data, function_index):
    MIN = functions[function_index]['MIN']
    MAX = functions[function_index]['MAX']
    DIMENSION = functions[function_index]['DIMENSION']
    V_BOUND = functions[function_index]['V_BOUND']
    POP_SIZE = functions[function_index]['POP_SIZE']
    PRECISION = functions[function_index]['PRECISION']
    MAX_TRIALS = functions[function_index]['MAX_TRIALS']

    employed_count = ceil(POP_SIZE / 2)
    onlocker_count = POP_SIZE - employed_count

    # for each employed bee
    for index, bee in bees[:employed_count].iterrows():
        # select a random dimension
        dimension = np.random.randint(0, DIMENSION)
        # select a random bee
        random_bee = bees.sample(1)
        # calculate the new position
        new_bee = bee.copy()
        new_bee[dimension] = new_bee[dimension] + np.random.rand() * (new_bee[dimension] - random_bee[dimension])


        # if the new position is out of bounds, set it to the bound
        if new_bee[dimension] < MIN:
            new_bee[dimension] = MIN
        elif new_bee[dimension] > MAX:
            new_bee[dimension] = MAX
        # if new fitness is better than old fitness, replace old position with new position
        new_fitness = functions[function_index]['f'](new_bee)
        if new_fitness < data['fitness'][index]-PRECISION:
            data['fitness'][index] = new_fitness
            bees.loc[index] = new_bee
        else:
            data['trial'][index] += 1
    return bees, data
#%%
def onlooker_bee_phase(bees, data, function_index):
    MIN = functions[function_index]['MIN']
    MAX = functions[function_index]['MAX']
    DIMENSION = functions[function_index]['DIMENSION']
    V_BOUND = functions[function_index]['V_BOUND']
    POP_SIZE = functions[function_index]['POP_SIZE']
    PRECISION = functions[function_index]['PRECISION']

    employed_count = ceil(POP_SIZE / 2)
    onlocker_count = POP_SIZE - employed_count

    # for each onlooker bee
    for index, bee in bees[employed_count:].iterrows():
        # select a random bee based on fitness
        random_bee = bees[:employed_count].sample(1, weights=data['fitness'])
        # select a random dimension
        dimension = np.random.randint(0, DIMENSION)
        # calculate the new position
        new_bee = bee.copy()
        new_bee[dimension] = new_bee[dimension] + np.random.rand() * (new_bee[dimension] - random_bee[dimension])
        # if the new position is out of bounds, set it to the bound
        if new_bee[dimension] < MIN:
            new_bee[dimension] = MIN
        elif new_bee[dimension] > MAX:
            new_bee[dimension] = MAX
        # if new fitness is better than old fitness, replace old position with new position
        new_fitness = functions[function_index]['f'](new_bee)
        if new_fitness < data['fitness'][index]:
            data['fitness'][index] = new_fitness
            bees.loc[index] = new_bee
    return bees, data['fitness']

def scout_bee_phase(bees, data, function_index):
    MIN = functions[function_index]['MIN']
    MAX = functions[function_index]['MAX']
    DIMENSION = functions[function_index]['DIMENSION']
    V_BOUND = functions[function_index]['V_BOUND']
    POP_SIZE = functions[function_index]['POP_SIZE']
    PRECISION = functions[function_index]['PRECISION']
    MAX_TRIALS = functions[function_index]['MAX_TRIALS']

    employed_count = ceil(POP_SIZE / 2)
    onlocker_count = POP_SIZE - employed_count

    # for each scout bee
    for index, bee in data[data['trial'] >= MAX_TRIALS].iterrows():
        # reset trial counter
        data['trial'][index] = 0
        # generate new random position
        bees.loc[index] = np.random.uniform(MIN, MAX, DIMENSION).round(1)
        # calculate new fitness
        data['fitness'][index] = functions[function_index]['f'](bees.loc[index])
    return bees, data
# %%
def run(function_index, enable_plot, maxiter=0):
    stat_data = []
    PRECISION = functions[function_index]['PRECISION']
    DIMENSION = functions[function_index]['DIMENSION']
    MAX = functions[function_index]['MAX']

    #fig = None
    #sc = None

    bees, data = init(function_index)
    functions[function_index]['MAX_TRIALS'] = functions[function_index]['POP_SIZE'] * functions[function_index]['DIMENSION']
    if enable_plot == 1:
        if DIMENSION == 2:
            fig, sc = init_2D_plot(bees)    
            plot2D(bees, fig, sc)
        if DIMENSION == 3:
            fig, sc = init_3D_plot(bees)
            plot3D(bees, fig, sc)
        if DIMENSION >= 4:
            fig, axs = init_plot(bees, DIMENSION, MAX)
            plot(bees, fig, axs, DIMENSION, MAX)
              
    best_fitness = []
    best_bee = []

    i = 1
    running = True
    while running:
        bees, data = employed_bee_phase(bees, data, function_index)
        bees, data['fitness'] = onlooker_bee_phase(bees, data, function_index)
        bees, data = scout_bee_phase(bees, data, function_index)
        best_fitness.append(data['fitness'].min())
        best_bee.append(bees.iloc[data['fitness'].idxmin()])
        if i % 100 == 0:
            print('Iteration: ' + str(i))
            print('Best fitness: ' + str(best_fitness[-1]))
            #print('Best bee: ' + str(best_bee[-1]))
            print('----------------------')
        if enable_plot == 1:
            if DIMENSION == 2:
                plot2D(bees, fig, sc)
            if DIMENSION == 3:
                plot3D(bees, fig, sc)
            if DIMENSION > 3 and i % 10 == 0:
                plot(bees, fig, axs, DIMENSION, MAX)
            fig.suptitle('i=' + str(i) + ' | f=' + str(round(best_fitness[-1], 4)), fontsize=30)

        if i % 10 == 0:
            stat_data.append([i, best_fitness[-1]])
        i += 1
        if best_fitness[-1] < PRECISION*2 or i == maxiter:
            running = False
    #fig.clear()
    return best_fitness, best_bee, stat_data

def init_2D_plot(bees):
    plt.ion()
    fig, ax = plt.subplots()
    x, y = bees[0], bees[1]
    plt.axis([functions[index]['MIN'], functions[index]['MAX'], functions[index]['MIN'], functions[index]['MAX']])
    sc = ax.scatter(x, y, c='r', s=50)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    return fig, sc
def plot2D(bees, fig, sc):
    x, y = bees[0], bees[1]
    sc.set_offsets(np.c_[x, y])
    fig.canvas.draw()
    fig.canvas.flush_events()
def init_3D_plot(bees):
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    x, y, z = bees[0], bees[1], bees[2]
    sc = ax.scatter(x, y, z)
    sleep(0.5)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    #plt.close(1)
    return fig, sc
def plot3D(bees, fig, sc):
    x, y, z = bees[0], bees[1], bees[2]
    sc._offsets3d = (x, y, z)
    fig.canvas.draw()
    fig.canvas.flush_events()
def init_plot(bees, DIMENSION, MAX):
    plt.ion()
    n = ceil(sqrt(functions[index]['DIMENSION']))
    fig, axs = plt.subplots(n, n, figsize=(7, 7))
    x = 0
    for i in range(0, n):
        for j in range(0, n):
            if x < DIMENSION:
                axs[i, j].hist(bees[x], density=True, bins=MAX, range=(-MAX, MAX))
                #set the y axis to 0 to 1
                axs[i, j].set_title(f'{x}')
            else:
                axs[i, j].axis('off')
            x += 1
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    return fig, axs
def plot(bees, fig, axs, DIMENSION, MAX):
    
    n = ceil(sqrt(functions[index]['DIMENSION']))
    maxima = bees.abs().max()
    x = 0
    for i in range(0, n):
        for j in range(0, n):
            if x < DIMENSION:
                axs[i, j].cla()
                axs[i, j].hist(bees[x], density=True, bins=max(20, int(MAX/2)), range=(min(-(MAX)/10, -maxima[x]), max(MAX/10, maxima[x])))
            x += 1
    fig.canvas.draw()
    fig.canvas.flush_events()
    return
#%%
if __name__ == "__main__":
    if int(input('Run analysis? (0,1)')) == 0:
        # get input from user for which function to run
        index = int(input('Enter the index of the function to run (0, 1, 2): '))
        # get input from user for the dimension of the function
        functions[index]['DIMENSION'] = int(input('Enter the dimension of the function: '))
        # get input from user for the number of particles
        functions[index]['POP_SIZE'] = int(input('Enter the number of particles: '))
        # get input for PRECISION
        functions[index]['PRECISION'] = float(input('Enter the precision: '))
        # get input for maxiter
        maxiter = int(input('Enter the max number of iterations: '))
        # run the algorithm
        enable_plot = int(input('Enable plot? (0,1): '))
            
        best_fitness, best_bee, data = run(index, enable_plot)
        
        print('Best fitness: ' + str(best_fitness[-1]))
        sleep(1)
        # plot the best fitness over the iterations
        # plt.plot(best_fitness)
        # plt.title('Best fitness over iterations')
        # plt.xlabel('Iteration')
        # plt.ylabel('Fitness')
        # plt.show()
        # wait for user to close plot
        input('Press enter to close plot')
    else:
        iterlim = 1500
        result = {}
        times = {}
        for i in range(len(functions)):
            print('function: ', i)
            # get system time
            start = time.time()
            best_bee, best_fitness, result[i] = run(i, 0, iterlim)
            end = time.time()
            times[i] = end - start



        # %%
        for i in range(0,len(functions)-1):
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
        #plt.ylim(0, 1000000)
        #plt.xlim(0, 400)
        plt.show()
# %%