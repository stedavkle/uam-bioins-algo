from json.encoder import INFINITY
from random import random, randrange, uniform

# function parameter
DIMENSION = 10
MIN = -100
MAX = 100
PRECISION = 0.01
DECIMAL_POINT = len(str(PRECISION).split('.')[1])


def f1(p):
    return sum([pow(x,2) for x in p.pos])

class particle:
    pos = []
    velocity = 0
    fitness = 0
    particleBestFitnessValue = []
    particleBestFitnessPos = []

    def __init__(self) -> None:
        self.pos = [round(uniform(MIN, MAX), DECIMAL_POINT) for i in range(0,DIMENSION)]
        self.velocity = [uniform(PRECISION, PRECISION*10) for i in range(0, DIMENSION)]
        self.fitness = f1(self)
        self.particleBestFitnessValue.append(self.fitness)
        self.particleBestFitnessPos.append(self.pos)

class universe:
    # Global best values
    GLOBAL_BEST_FITNESS_VALUE = INFINITY
    GLOBAL_BEST_FITNESS_POS = [round(uniform(MIN, MAX), DECIMAL_POINT) for i in range(0,DIMENSION)]

    population = []
    # on construct initialize with all parameters given in function header
    def __init__(self, pop_size, iterations, inertia, cognition, influence) -> None:
        self.POP_SIZE = pop_size
        self.ITERATIONS = iterations
        self.INERTIA = inertia
        self.COGNITION = cognition
        self.INFLUENCE = influence

    def init(self):
        self.population = [particle() for i in range(0, self.POP_SIZE)]
    def optimize(self):
        for i in range(0, self.ITERATIONS):
            if i % 100 == 0:
                print("Iteration: ", i)
            for p in self.population:
                # Update velocity using list comprehension
                p.velocity = [min(PRECISION*10, max(PRECISION,
                                round(self.INERTIA * p.velocity[i]
                                + self.COGNITION * random() * (p.particleBestFitnessPos[-1][i] - p.pos[i])
                                + self.INFLUENCE * random() * (self.GLOBAL_BEST_FITNESS_POS[i] - p.pos[i]), DECIMAL_POINT))) for i in range(0, DIMENSION)]
                # update position
                p.pos = [round(p.pos[i] + p.velocity[i], DECIMAL_POINT) for i in range(0, DIMENSION)]
                # update fitness if new position is better
                if f1(p) < p.fitness:
                    p.fitness = f1(p)
                    p.particleBestFitnessValue.append(p.fitness)
                    p.particleBestFitnessPos.append(p.pos)
                    # update global best if new position is better
                    if p.fitness < self.GLOBAL_BEST_FITNESS_VALUE:
                        self.GLOBAL_BEST_FITNESS_VALUE = p.fitness
                        self.GLOBAL_BEST_FITNESS_POS = p.pos
    def get_solution(self):
        return (self.GLOBAL_BEST_FITNESS_POS, self.GLOBAL_BEST_FITNESS_VALUE)

if __name__ == "__main__":
    # Universe params
    POP_SIZE = 204
    ITERATIONS = 5000
    INERTIA = -0.2134
    COGNITION = -0.3344
    INFLUENCE = 4.8976

    u = universe(POP_SIZE, ITERATIONS, INERTIA, COGNITION, INFLUENCE)
    u.init()
    u.optimize()
    print(u.get_solution())