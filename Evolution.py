# coding=utf-8
import numpy as np
import define

def get_fitness(scores, times):
    return 3 * np.array(scores) + np.array(times)

def translateDNA(DNAS):
    print(DNAS)
    threholds = [DNA[:define.THREHOLD_SIZE] for DNA in DNAS]
    hungers = [DNA[define.THREHOLD_SIZE:(define.THREHOLD_SIZE + define.HUNGER_SIZE)] for DNA in DNAS]
    alives = [DNA[-define.ALIVE_SIZE:] for DNA in DNAS]

    threholds = [int(threhold, 2) for threhold in threholds]
    hungers = [int(hunger, 2) for hunger in hungers]
    alives = [int(alive, 2) for alive in alives]
    # print(threholds)
    return threholds[0], hungers[0], alives[0]

def select(snakes, fitness):
    print(len(snakes),len(fitness))
    idx = np.random.choice(np.arange(len(snakes)),size= len(snakes), p=fitness/fitness.sum())
    # print(snakes)
    return np.array(snakes)[idx]

def crossover(parent, snakes):     # mating process (genes crossover)
    if np.random.rand() < define.CROSS_RATE:
        i = np.random.randint(0, define.POP_SIZE)  # select another individual from pop
        cross_point = np.random.randint(0, define.DNA_SIZE - 1)  # 随机产生一个交叉点
        print ("cross_point", cross_point)
        temporary1 = []
        temporary2 = []
        temporary1.extend(snakes[i][0:cross_point])
        temporary1.extend(parent[cross_point:len(snakes[i])])

        temporary2.extend(parent[0:cross_point])
        temporary2.extend(snakes[i][cross_point:len(snakes[i])])
        parent = temporary2

    return parent

def mutate(child):
    for point in range(define.DNA_SIZE):
        if np.random.rand() < define.MUTATION_RATE:
            child[point].replace('0', '1')
            child[point].replace('1', '0')
    return child

if __name__ == '__main__':
    DNAS = ["10101010101010101010"]

    threhold, hungers, alives = translateDNA(DNAS)

    print(threhold, hungers, alives)
