from import_data import fetch_structure_data
from random import choice
from pprint import pprint
from transponder_set import transponder_set

EPOCHS = 10
TRANSPONDERS = (0, 100, 200, 400)

def init_population(demands_, population_count):
    population = []
    chromosome = {}
    for _ in range(population_count):
        for demand in demands_:
            chromosome[demand] = []
            possible_transponders = transponder_set(int(demands_[demand][2].removesuffix(".0")))
            for path in demands_[demand][3]:
                chromosome[demand].append((path, choice(TRANSPONDERS)))
        population.append(chromosome)
    return population
    # chromosome[demand].append((path, choice(transponder_set(int(demands_[demand][2].removesuffix(".0"))))))


def evaluate(chromosome, demands):
    capacity_too_high_param = 1
    capacity_too_low_param = 10
    lambda_penalty = 100
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
    for demand in chromosome:
        transponder_capacity_sum = 0
        for path, transponder_capacity in chromosome[demand]:
            if transponder_capacity > 0:
                transponder_capacity_sum += transponder_capacity
                for link in path:
                    links[link] += 1
        target_demand = int(demands[demand][2].removesuffix(".0"))
        if transponder_capacity_sum > target_demand:  # kara za za duza przepustowość
            penalty += capacity_too_high_param * (transponder_capacity_sum - target_demand)
        elif transponder_capacity_sum < target_demand:  # kara za za mala przepustowość
            penalty += capacity_too_low_param * (target_demand - transponder_capacity_sum)
    for lambdas_used in links.values():
        if lambdas_used > 96:
            penalty += lambda_penalty * lambdas_used
    return penalty


def loop():
    for epoch in range(EPOCHS):
        pass


if __name__ == '__main__':
    nodes_, links_, demands_ = fetch_structure_data("polska.xml")
    population = init_population(demands_, 1)
    print(evaluate(population[0], demands_))
    pprint(demands_)
