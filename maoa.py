import random
import numpy as np
import matplotlib.pyplot as plt

from data.dataset import Dataset
from target_metrics import compute_metrics


def target_functions(problem, solution):
    """
    Calcule les valeurs des fonctions objectif.
    Args:
        problem : objet dataset
            Contient les informations sur les tâches et les machines.
        solution : tableau binaire de forme (n_tasks, n_machines)
            Matrice binaire indiquant l'affectation des tâches aux machines.
    Returns:
        Tableau des valeurs des fonctions objectif (makespan, coût).
    """
    makespan, cost = compute_metrics(problem, solution)
    return np.array([makespan, cost])

def dominates(sol1, sol2):
    """Vérifie si sol1 domine sol2.
    Args:
        sol1 : np.array
            Valeurs des fonctions objectif pour la première solution.
        sol2 : np.array
            Valeurs des fonctions objectif pour la deuxième solution.
    Returns:
        True si sol1 domine sol2, sinon False.
    """
    return np.all(sol1 <= sol2) and np.any(sol1 < sol2)

def non_dominated_sort(population):
    """Trouve les solutions non dominées.
    Args:
        population : list de tuples (solution, valeurs_objectif)
            Une liste où chaque élément contient une solution et ses valeurs de fonction objectif.
    Returns:
        Tableau contenant les solutions non dominées.
    """
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

def initialize_population(size, n, p, problem):
    # Extra columns for objectives
    population = np.zeros((size, n * p + 2))  
    for i in range(size):
        matrix = np.zeros((n, p))
        for row in range(n):
            # Ensure one 1 per row
            matrix[row, random.randint(0, p - 1)] = 1  
        population[i, :-2] = matrix.flatten()
        population[i, -2:] = target_functions(problem, matrix)
    return population

def repair_solution(solution, n, p):
    # Ensure each row has exactly one 1.
    matrix = solution.reshape(n, p)
    for row in range(n):
        # sigmoid function to enforce binary values
        matrix[row] = np.round(1 / (1 + np.exp(-matrix[row])))
        if np.sum(matrix[row]) != 1:
            # Randomly choose a 1 to keep
            ones = np.where(matrix[row] == 1)[0]
            if len(ones) > 1:
                idx = random.choice(ones)
            else:
                idx = random.randint(0, p - 1)
            # Reset row
            matrix[row] = 0 
            # Keep chosen 1
            matrix[row, idx] = 1
    return matrix.flatten()

def update_population(population, archive, mu, moa, mop, n, p, problem):
    # Small value to prevent division by zero
    e = 1e-15 
    p_new = np.copy(population)
    for i in range(population.shape[0]):
        # Choose leader from archive
        leader = random.choice(archive)[:-2]  
        for j in range(n * p):
            r1, r2, r3 = random.random(), random.random(), random.random()
            if r1 > moa:
                # Exploration Step
                if r2 > 0.5:
                    p_new[i, j] = leader[j] / (mop + e)
                else:
                    p_new[i, j] = leader[j] * mop * mu
            else:
                # Exploitation Step
                if r3 > moa:
                    if r2 > 0.5:
                        p_new[i, j] = leader[j] - (mop * mu)
                    else:
                        p_new[i, j] = leader[j] + (mop * mu)
        p_new[i, :-2] = repair_solution(p_new[i, :-2], n, p)
        p_new[i, -2:] = target_functions(problem, p_new[i, :-2].reshape(n, p))
    return p_new

def run_moaoa(problem, size=10, n=5, p=5, iterations=50, alpha=0.5, mu=5, verbose=True):
    population = initialize_population(size, n, p, problem)
    archive = non_dominated_sort(population)
    for count in range(iterations):
        if verbose:
            print(f'Iteration {count}, Archive Size: {len(archive)}')
        moa = 0.2 + count * ((1 - 0.2) / iterations)
        mop = 1 - ((count ** (1 / alpha)) / (iterations ** (1 / alpha)))
        population = update_population(population, archive, mu, moa, mop, n, p, problem)
        # Merge and sort solutions
        archive = non_dominated_sort(np.vstack((archive, population))) 
        if len(archive) > size:
            # Keep archive size manageable
            archive = archive[:size]  
    return archive

def plot_pareto_front(archive):
    archive = archive[np.argsort(archive[:, -2])]
    plt.scatter(archive[:, -2], archive[:, -1])
    plt.plot(archive[:, -2], archive[:, -1], linestyle="dotted", color="blue", alpha=0.7)
    plt.xlabel('Makespan')
    plt.ylabel('Cost')
    plt.title('Pareto Front')
    plt.show()

if __name__ == '__main__':
    dataset = Dataset(n_machines=5, n_tasks=10)
    dataset.plot()
    archive = run_moaoa(problem=dataset, n=10, p=5, iterations=100, verbose=True)
    print(archive)
    print(f'Archive Size: {len(archive)}')
    plot_pareto_front(archive)
    dataset.plot_schedule()
