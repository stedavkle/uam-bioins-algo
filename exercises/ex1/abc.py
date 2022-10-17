#%%
import pandas as pd
import numpy as np
from math import ceil, prod, sqrt, floor

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
def init(function_index):
    MIN = functions[function_index]['MIN']
    MAX = functions[function_index]['MAX']
    DIMENSION = functions[function_index]['DIMENSION']
    V_BOUND = functions[function_index]['V_BOUND']
    POP_SIZE = functions[function_index]['POP_SIZE']
    PRECISION = functions[function_index]['PRECISION']

    employed_count = ceil(POP_SIZE / 2)
    onlocker_count = POP_SIZE - employed_count


    # # create a pandas dataframe with as many rows as particles and as many columns as dimensions
    # employed_bees = pd.DataFrame(np.random.uniform(MIN, MAX, (employed_count, DIMENSION)).round(1))
    # onlooker_bees = pd.DataFrame(np.random.uniform(MIN, MAX, (onlocker_count, DIMENSION)).round(1))
    # # add columns for fitness to employed_bees and onlooker_bees
    # employed_bees['fitness'] = employed_bees.apply(lambda row: functions[function_index]['f'](row), axis=1)
    # onlooker_bees['fitness'] = onlooker_bees.apply(lambda row: functions[function_index]['f'](row), axis=1)
    bees = pd.DataFrame(np.random.uniform(MIN, MAX, (POP_SIZE, DIMENSION)).round(1))
    fitness = bees.apply(lambda row: functions[function_index]['f'](row), axis=1)

    return bees, fitness
#%%
def employed_bee_phase(bees, fitness, function_index):
    MIN = functions[function_index]['MIN']
    MAX = functions[function_index]['MAX']
    DIMENSION = functions[function_index]['DIMENSION']
    V_BOUND = functions[function_index]['V_BOUND']
    POP_SIZE = functions[function_index]['POP_SIZE']
    PRECISION = functions[function_index]['PRECISION']

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
        if new_fitness < fitness[index]:
            fitness[index] = new_fitness
            bees.loc[index] = new_bee
    return bees, fitness


# %%
bees, fitness = init(0)
employed_bee_phase(bees, fitness, 0)
# %%
