import numpy as np
import random
import os

from dataset import Dataset
from target_metrics import compute_metrics

dataset = Dataset(n_machines=5, n_tasks=10)

def target_functions(solution):
    """
    Define multiple objective functions. Replace these with actual objectives.
    """
    makespan, cost = compute_metrics(dataset, solution)
    return np.array([makespan, cost])

def dominates(sol1, sol2):
    """Check if sol1 dominates sol2."""
    return np.all(sol1 <= sol2) and np.any(sol1 < sol2)

def non_dominated_sort(population):
    """Find non-dominated solutions."""
    archive = []
    for sol in population:
        dominated = False
        for arch_sol in archive:
            if dominates(arch_sol[-1], sol[-1]):
                dominated = True
                break
        if not dominated:
            archive.append(sol)
    return np.array(archive)

def initialize_population(size, n, p):
    population = np.zeros((size, n * p + 2))  # Extra columns for objectives
    for i in range(size):
        matrix = np.zeros((n, p))
        for row in range(n):
            matrix[row, random.randint(0, p - 1)] = 1  # Ensure one 1 per row
        population[i, :-2] = matrix.flatten()
        population[i, -2:] = target_functions(matrix)
    return population

def repair_solution(solution, n, p):
    """Ensure each row has exactly one 1."""
    matrix = solution.reshape(n, p)
    for row in range(n):
        if np.sum(matrix[row]) != 1:
            matrix[row] = 0  # Reset row
            matrix[row, random.randint(0, p - 1)] = 1  # Place a single 1
    return matrix.flatten()

def update_population(population, archive, mu, moa, mop, n, p):
    p_new = np.copy(population)
    for i in range(population.shape[0]):
        leader = random.choice(archive)[:-2]  # Choose leader from archive
        for row in range(n):
            if random.random() > moa:
                chosen_col = np.argmax(leader[row * p:(row + 1) * p])  # Copy leader's column
                p_new[i, row * p:(row + 1) * p] = 0
                p_new[i, row * p + chosen_col] = 1
            else:
                chosen_col = random.randint(0, p - 1)
                p_new[i, row * p:(row + 1) * p] = 0
                p_new[i, row * p + chosen_col] = 1
        p_new[i, :-2] = repair_solution(p_new[i, :-2], n, p)
        p_new[i, -2:] = target_functions(p_new[i, :-2].reshape(n, p))
    return p_new

def moaoa(size=10, n=5, p=5, iterations=50, alpha=0.5, mu=5, verbose=True):
    population = initialize_population(size, n, p)
    archive = non_dominated_sort(population)
    for count in range(iterations):
        if verbose:
            print(f'Iteration {count}, Archive Size: {len(archive)}')
        moa = 0.2 + count * ((1 - 0.2) / iterations)
        mop = 1 - ((count ** (1 / alpha)) / (iterations ** (1 / alpha)))
        population = update_population(population, archive, mu, moa, mop, n, p)
        archive = non_dominated_sort(np.vstack((archive, population)))  # Merge and sort solutions
        if len(archive) > size:
            archive = archive[:size]  # Keep archive size manageable
    return archive

def plot_pareto_front(archive):
    import matplotlib.pyplot as plt
    plt.scatter(archive[:, -2], archive[:, -1])
    plt.xlabel('Makespan')
    plt.ylabel('Cost')
    plt.title('Pareto Front')
    plt.show()

if __name__ == '__main__':
    archive = moaoa(n=10, p=5, iterations=100, verbose=False)
    print(archive)
    print(f'Archive Size: {len(archive)}')
    plot_pareto_front(archive)
