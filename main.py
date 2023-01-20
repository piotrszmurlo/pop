from import_data import fetch_structure_data
from random import choice
from pprint import pprint
from transponder_set import transponder_set

EPOCHS = 10
LAMBDA_PENALTY = 100
TRANSPONDER_COST = {
    40: 1,
    60: 3,
    80: 7
}


def init_population(demands_, population_count):
    population = []
    chromosome = {}
    for _ in range(population_count):
        for demand in demands_:
            chromosome[demand] = []
            possible_transponder_sets = transponder_set(int(demands_[demand][2].removesuffix(".0")))
            transponder_set_ = choice(possible_transponder_sets)
            paths = demands_[demand][3]
            for transponder in transponder_set_:
                chromosome[demand].append((choice(paths), transponder))
        population.append(chromosome)
    return population


def evaluate(chromosome, demands):
    penalty = 0
    links = {'Link_0_10': 0,
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
             'Link_7_9': 0}
    total_cost = 0
    for demand in chromosome:
        demand_cost = 0
        for path, transponders in chromosome[demand]:
            demand_cost += TRANSPONDER_COST[transponders]
            for link in path:
                links[link] += 1
        total_cost += demand_cost
    for lambdas_used in links.values():
        if lambdas_used > 96:
            penalty += LAMBDA_PENALTY * lambdas_used
    penalty += total_cost
    return penalty


def loop():
    for epoch in range(EPOCHS):
        pass


if __name__ == '__main__':
    nodes_, links_, demands_ = fetch_structure_data("polska.xml")
    population = init_population(demands_, 1)
    pprint(evaluate(population[0], demands_))
    # pprint(population[0])
