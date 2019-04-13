import numpy as np
import define


def get_fitness(score, time):  # 适应度函数

    return 3 * score / time


def translateDNA(DNAS):
    threholds = [DNA[:define.THREHOLD_SIZE] for DNA in DNAS]
    hungers = [DNA[define.THREHOLD_SIZE:(define.THREHOLD_SIZE + define.HUNGER_SIZE)] for DNA in DNAS]
    alives = [DNA[-define.ALIVE_SIZE:] for DNA in DNAS]

    threholds = [int(threhold, 2) for threhold in threholds]
    hungers = [int(hunger, 2) for hunger in hungers]
    alives = [int(alive, 2) for alive in alives]

    return threholds, hungers, alives


if __name__ == '__main__':
    DNAS = ["10101010101010101010"]

    threhold, hungers, alives = translateDNA(DNAS)

    print(threhold, hungers, alives -)
