import random
from pprint import pprint
from random import choice, sample, shuffle, randrange
from copy import deepcopy
from import_data import fetch_structure_data
from transponder_set import transponder_set, TRANSPONDER_COST

EPOCHS = 10
LAMBDA_PENALTY = 100
POPULATION_SIZE = 10
ELITE_SIZE = 0.2
CROSS_P = 0.7
MUTATE_P = 0.2


def init_population(demands_, population_count):
    population = []
    for _ in range(population_count):
        chromosome = {}
        for demand in demands_:
            chromosome[demand] = []
            possible_transponder_sets = transponder_set(int(demands_[demand][2].removesuffix(".0")))
            transponder_set_ = choice(possible_transponder_sets)
            paths = demands_[demand][3]
            for transponder in transponder_set_:
                chromosome[demand].append((choice(paths), transponder))
        population.append(chromosome)
    return population


def evaluate(chromosome):
    penalty = 0
    links = {
        'Link_0_10': 0,
        'Link_0_2': 0,
        'Link_0_5': 0,
        'Link_1_10': 0,
        'Link_1_2': 0,
        'Link_1_7': 0,
        'Link_2_9': 0,
        'Link_3_11': 0,
        'Link_3_4': 0,
        'Link_3_6': 0,
        'Link_4_10': 0,
        'Link_4_8': 0,
        'Link_5_10': 0,
        'Link_5_8': 0,
        'Link_6_10': 0,
        'Link_6_11': 0,
        'Link_7_11': 0,
        'Link_7_9': 0
    }
    total_cost = 0
    for demand in chromosome:
        demand_cost = 0
        for path, transponders in chromosome[demand]:
            demand_cost += TRANSPONDER_COST[transponders]
            for link in path:
                links[link] += 1
        total_cost += demand_cost
    for lambdas_used in links.values():
        if lambdas_used > 80:
            penalty += LAMBDA_PENALTY * lambdas_used
    penalty += total_cost
    return penalty


def reproduce(population):
    penalties = [(index, evaluate(chromosome)) for index, chromosome in enumerate(population)]
    # sum_penalties = 0
    # for penalty in penalties:
    #     sum_penalties += 1/penalty
    # fit_list = []
    # for index, chromosome in enumerate(population):
    #     fit_list.append((1/penalties[index])/sum_penalties)
    new_population = []
    while len(new_population) != len(population):
        x, y = sample(penalties, 2)
        if x[1] >= y[1]:
            new_population.append(population[y[0]])
        else:
            new_population.append(population[x[0]])
    return new_population

def cross_and_mutate(population):
    cross_population = deepcopy(population)
    cross_population = cross_population[:(2*int(len(cross_population)*CROSS_P))//2 + 1]
    new_population = []
    while len(cross_population) > 0:
        id_1 = randrange(0, len(cross_population))
        chrom_1 = cross_population.pop(id_1)
        id_2 = randrange(0, len(cross_population))
        chrom_2 = cross_population.pop(id_2)
        new_chrom_1 = {}
        new_chrom_2 = {}
        r = random.randint(1, 66)
        i = 0
        for key, value in chrom_2.items():
            if i < r:
                new_chrom_1[key] = value
            if i >= r:
                new_chrom_2[key] = value
            i += 1
        i = 0
        for key, value in chrom_1.items():
            if i < r:
                new_chrom_2[key] = value
            if i >= r:
                new_chrom_1[key] = value
            i += 1
        new_population.append(new_chrom_1)
        new_population.append(new_chrom_1)
    new_population += cross_population[(2*int(len(cross_population)*CROSS_P))//2 + 1:]
    return new_population

def loop():
    population = init_population(demands_, POPULATION_SIZE)
    new_population = reproduce(population)
    for f in population:
        print(evaluate(f))
    print("------------------------------------")
    for f in new_population:
        print(evaluate(f))
    cross_population = cross_and_mutate(population)
    print(len(cross_population))
    for epoch in range(EPOCHS):
        new_population = population
        # mutacja

        # rekombinacja
        pass


if __name__ == '__main__':
    nodes_, links_, demands_ = fetch_structure_data("polska.xml")
    loop()
    # pprint(population[0])
