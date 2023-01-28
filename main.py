import random
from pprint import pprint
from random import choice, sample, shuffle, randrange
from copy import deepcopy
from import_data import fetch_structure_data
from transponder_set import transponder_set, TRANSPONDER_COST
from export_data import export_data
from os.path import join
import matplotlib.pyplot as plt

PLOT_PATH = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/wykresy"

EPOCHS = 20
LAMBDA_PENALTY = 100
POPULATION_SIZE = 10
ELITE_SIZE = 0
CROSS_P = 0.7
MUTATE_P = 0.1
MAX_LAMBDAS_USED = 70


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


def evaluate(chromosome, print_if_lambdas_exceeded=False):
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
            demand_cost += TRANSPONDER_COST[transponders]*2
            for link in path:
                links[link] += 1
        total_cost += demand_cost
    for lambdas_used in links.values():
        if lambdas_used > MAX_LAMBDAS_USED:
            penalty += LAMBDA_PENALTY * lambdas_used
            if print_if_lambdas_exceeded:
                print("Chromosome exceeds lambda capacity")
    penalty += total_cost
    return penalty


def selection(population):
    penalties = [(index, evaluate(chromosome)) for index, chromosome in enumerate(population)]
    sorted_penalties = sorted(penalties, key=lambda t: t[1])
    new_population = []
    for i in range(ELITE_SIZE):
        new_population.append(population[sorted_penalties[i][0]])
    while len(new_population) != len(population):
        x, y = sample(penalties, 2)
        if x[1] >= y[1]:
            new_population.append(population[y[0]])
        else:
            new_population.append(population[x[0]])
    return new_population


def cross(population):
    cross_population = deepcopy(population)
    temp_cross_population = []
    crosses_num = int(len(population) * CROSS_P)
    if crosses_num % 2 == 1:
        crosses_num -= 1
    indv_ids = list(range(len(population)))
    # creation of list of individuals that will be crossed
    for i in range(crosses_num):
        r = random.randrange(len(indv_ids))
        ind_id = indv_ids.pop(r)
        temp_cross_population.append(cross_population[ind_id])

    # creation of list of individuals that will remain uncrossed
    uncrossed_individuals = []
    for i in indv_ids:
        uncrossed_individuals.append(cross_population[i])

    cross_population = temp_cross_population
    crossed_population = []
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
        crossed_population.append(new_chrom_1)
        crossed_population.append(new_chrom_1)
    crossed_population += uncrossed_individuals
    return crossed_population


def mutate(population, demands_):
    mutate_population = deepcopy(population)
    for i in range(len(mutate_population)):
        for dem_id, demand in mutate_population[i].items():
            if random.random() < MUTATE_P:
                possible_transponder_sets = transponder_set(int(demands_[dem_id][2].removesuffix(".0")))
                transponder_set_ = choice(possible_transponder_sets)
                paths = demands_[dem_id][3]
                new_gene = []
                for transponder in transponder_set_:
                    new_gene.append((choice(paths), transponder))
                mutate_population[i][dem_id] = new_gene
    return mutate_population


def create_new_population(population, demands_):
    # reproduction
    selected_population = selection(population)
    # crossing
    crossed_population = cross(selected_population)
    # mutation
    muted_population = mutate(crossed_population, demands_)
    return muted_population


def get_best_individual(population):
    best_eval = 10000000
    best_individual = 0
    for i in range(len(population)):
        temp_eval = evaluate(population[i])
        if temp_eval <= best_eval:
            best_eval = temp_eval
            best_individual = i
    return population[best_individual]


def plot_best(best_solutions):
    epochs = range(1, len(best_solutions) + 1)
    plt.plot(epochs, best_solutions)
    plt.xlabel('Epoki')
    plt.ylabel('Funkcja dopasowania')
    plt.title('najlepszy osobnik z populacji: ' +
              'epoki: ' + str(EPOCHS) + " pop.: " + str(POPULATION_SIZE) + " kara: " + str(LAMBDA_PENALTY) +
              ' cross r.: ' + str(CROSS_P) + ' mut.r.: ' + str(MUTATE_P))
    plt.show()
    transponders_capacities = list(TRANSPONDER_COST.keys())
    plot_name = ["epoki: ", str(EPOCHS), " pop.: ", str(POPULATION_SIZE), " kara: ", str(LAMBDA_PENALTY),
                 " cross r.: ", str(CROSS_P), " mut.r.: ", str(MUTATE_P), " tr.1: ", str(transponders_capacities[0]),
                 " tr.2: ", str(transponders_capacities[1]), " tr.3: ", str(transponders_capacities[2]), ".png"]
    path_suf = ""
    for p in plot_name:
        path_suf += p
    path = join(PLOT_PATH, path_suf)
    # print("PLOT PATH")
    # print(path)

    # plt.savefig(path)

def plot_best_min(best_solutions_min):
    epochs = range(1, len(best_solutions_min) + 1)
    plt.plot(epochs, best_solutions_min)
    plt.xlabel('Epoki')
    plt.ylabel('Funkcja dopasowania')
    plt.title('Najlepszy osobnik: ' +
              'epoki: ' + str(EPOCHS) + " pop.: " + str(POPULATION_SIZE) + " kara: " + str(LAMBDA_PENALTY) +
              ' cross r.: ' + str(CROSS_P) + ' mut.r.: ' + str(MUTATE_P))
    plt.show()
    transponders_capacities = list(TRANSPONDER_COST.keys())
    plot_name = ["epoki: ", str(EPOCHS), " pop.: ", str(POPULATION_SIZE), " kara: ", str(LAMBDA_PENALTY),
                 " cross r.: ", str(CROSS_P), " mut.r.: ", str(MUTATE_P), " tr.1: ", str(transponders_capacities[0]),
                 " tr.2: ", str(transponders_capacities[1]), " tr.3: ", str(transponders_capacities[2]), ".png"]
    path_suf = ""
    for p in plot_name:
        path_suf += p
    path = join(PLOT_PATH, path_suf)
    # print("PLOT PATH")
    # print(path)


def loop():
    best_solutions = []
    best_solutions_min_solution = []
    population = init_population(demands_, POPULATION_SIZE)
    for epoch in range(EPOCHS):
        print("------------------------------------------")
        print("EPOCH: " + str(epoch))
        new_population = create_new_population(population, demands_)
        population = new_population
        best_individual = get_best_individual(population)
        best_fit_individual = evaluate(best_individual, True)
        best_solutions.append(best_fit_individual)
        if all(element > best_fit_individual for element in best_solutions_min_solution):
            best_solutions_min_solution.append(best_fit_individual)
        else:
            best_solutions_min_solution.append(best_solutions_min_solution[-1])
        print("BEST INDIVIDUAL FIT FUNCTION")
        print(best_solutions_min_solution[-1])
    plot_best(best_solutions)
    plot_best_min(best_solutions_min_solution)
    print(f"FINAL BEST SOLUTION FIT: {best_solutions_min_solution[-1]}")


if __name__ == '__main__':
    nodes_, links_, demands_ = fetch_structure_data("polska.xml")
    loop()
