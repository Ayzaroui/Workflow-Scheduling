import random
import numpy as np
import matplotlib.pyplot as plt

from data.dataset import Dataset
from target_metrics import compute_metrics

def target_functions(solution, dataset):
    """
    Calcule les valeurs des fonctions objectif.
    """
    makespan, cost = compute_metrics(dataset, solution)
    return np.array([makespan, cost])

def dominates(sol1, sol2):
    return np.all(sol1 <= sol2) and np.any(sol1 < sol2)

def fast_non_dominated_sort(population):
    """
    Effectue un tri non dominé de NSGA-II.
    """
    fronts = [[]]
    domination_count = np.zeros(len(population))
    dominated_solutions = [[] for _ in range(len(population))]
    
    for p in range(len(population)):
        for q in range(len(population)):
            if dominates(population[p][-1], population[q][-1]):
                dominated_solutions[p].append(q)
            elif dominates(population[q][-1], population[p][-1]):
                domination_count[p] += 1
        if domination_count[p] == 0:
            fronts[0].append(p)
    
    i = 0
    while len(fronts[i]) > 0:
        next_front = []
        for p in fronts[i]:
            for q in dominated_solutions[p]:
                domination_count[q] -= 1
                if domination_count[q] == 0:
                    next_front.append(q)
        i += 1
        fronts.append(next_front)
    
    return fronts[:-1]

def crowding_distance_assignment(front, population):
    """
    Assigne des distances de dispersion pour le tri par encombrement.
    """
    distances = np.zeros(len(front))
    for m in range(2):  # Deux objectifs (makespan, cost)
        front.sort(key=lambda x: population[x][-1][m])
        distances[0] = distances[-1] = np.inf
        for i in range(1, len(front) - 1):
            distances[i] += (population[front[i + 1]][-1][m] - population[front[i - 1]][-1][m])
    return distances

def initialize_population(size, n, p, dataset):
    population = []
    for _ in range(size):
        solution = np.zeros((n, p))
        for row in range(n):
            solution[row, random.randint(0, p - 1)] = 1
        objectives = target_functions(solution, dataset)
        population.append((solution, objectives))
    return population

def tournament_selection(population, k=2):
    """
    Sélection par tournoi entre k individus.
    """
    selected = random.sample(population, k)
    return min(selected, key=lambda x: x[-1].sum())

def crossover(parent1, parent2):
    """
    Croisement unidimensionnel entre deux parents.
    """
    child = np.copy(parent1[0])
    point = random.randint(0, child.size - 1)
    child.flat[:point] = parent2[0].flat[:point]
    return child

def mutate(solution, mutation_rate=0.1):
    """
    Mutation en changeant l'affectation d'une tâche.
    """
    for i in range(solution.shape[0]):
        if random.random() < mutation_rate:
            solution[i] = 0
            solution[i, random.randint(0, solution.shape[1] - 1)] = 1
    return solution

def nsga2(size=10, n=5, p=5, generations=50, mutation_rate=0.1):
    dataset = Dataset(n_machines=n, n_tasks=p)
    population = initialize_population(size, n, p, dataset)
    
    for _ in range(generations):
        offspring = []
        for _ in range(size):
            p1, p2 = tournament_selection(population), tournament_selection(population)
            child_solution = crossover(p1, p2)
            child_solution = mutate(child_solution, mutation_rate)
            child_objectives = target_functions(child_solution, dataset)
            offspring.append((child_solution, child_objectives))
        
        combined_population = population + offspring
        fronts = fast_non_dominated_sort(combined_population)
        new_population = []
        for front in fronts:
            if len(new_population) + len(front) > size:
                distances = crowding_distance_assignment(front, combined_population)
                sorted_front = sorted(front, key=lambda x: distances[x], reverse=True)
                new_population.extend([combined_population[i] for i in sorted_front[:size - len(new_population)]])
                break
            else:
                new_population.extend([combined_population[i] for i in front])
        
        population = new_population
    
    return np.array([ind for ind in population])

def plot_pareto_front(archive, title="Pareto Front"):
    plt.scatter(archive[:, -2], archive[:, -1], label="Solutions")
    plt.xlabel("Makespan")
    plt.ylabel("Cost")
    plt.title(title)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    nsga2_archive = nsga2(n=10, p=5, generations=100)
    print(f'NSGA-II Archive Size: {len(nsga2_archive)}')
    plot_pareto_front(nsga2_archive, title="Pareto Front - NSGA-II")