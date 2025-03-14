import random
import numpy as np
import matplotlib.pyplot as plt

from data.randomDataset import RandomDataset
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
            if dominates(arch_sol[-2:], sol[-2:]):
                dominated = True
                break
        if not dominated:
            archive.append(sol)
        for arch_sol in archive: 
            # Remove solutions dominated by the newly added solution
            if dominates(sol[-2:], arch_sol[-2:]):
                archive = [a for a in archive if not np.array_equal(a, arch_sol)]
    return np.array(archive)

def initialize_population(size, problem):
    n = problem.n_tasks
    p = problem.n_machines
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

def compute_grid(solutions, num_bins=10):
    # use np.histogram to compute the grid for each objective
    grid = [list(np.histogram(solutions[:, i], bins=num_bins)[1]) for i in range(solutions.shape[1])]
    return np.array(grid)

def count_in_grid(solutions, grid):
    # count the number of solutions in each grid cell
    grid_counts = np.zeros([len(axis) - 1 for axis in grid])
    grid_indices = []
    for solution in solutions:
        idx = [np.digitize([solution[i]], grid[i])[0]-1 for i in range(solutions.shape[1])]
        # handle solutions on the right edge of the grid
        idx = [int(min(i, len(axis)-2)) for i, axis in zip(idx, grid)]
        grid_counts[tuple(idx)] += 1
        grid_indices.append(idx)
    return grid_indices, grid_counts

def leader_selection(archive, grid, C=2):
    indices, hypercube_counts = count_in_grid(archive[:, -2:], grid)
    # Select hypercube (lower population -> higher probability)
    probabilities = np.array([C/count if count>0 else 0 for count in hypercube_counts.flatten()])
    probabilities /= np.sum(probabilities)
    hypercude_idx = np.random.choice(len(probabilities), p=probabilities)
    hypercude_idx = np.unravel_index(hypercude_idx, hypercube_counts.shape) # convert to 2D index
    hypercude_idx = [int(i) for i in hypercude_idx] # convert to integers
    # Select a random solution from the chosen hypercube
    solutions_in_hypercube = [sol for i, sol in enumerate(archive) if indices[i] == hypercude_idx]
    sol_idx = np.random.choice(len(solutions_in_hypercube))

    return solutions_in_hypercube[sol_idx]

def update_population(population, archive, grid, mu, moa, mop, problem):
    n = problem.n_tasks
    p = problem.n_machines
    # Small value to prevent division by zero
    e = 1e-15 
    p_new = np.copy(population)
    for i in range(population.shape[0]):
        # Choose leader from archive
        leader = leader_selection(archive, grid)
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

def run_moaoa(problem, size=10, iterations=50, alpha=0.5, mu=5, n_bins=10, verbose=True):
    population = initialize_population(size, problem)
    archive = non_dominated_sort(population)
    grid = compute_grid(archive[:, -2:], n_bins)
    for count in range(iterations):
        if verbose:
            print(f"Iteration {count},  best cost: {archive[:, -1].min()}, best makespan: {archive[:, -2].min()}, Archive Size: {len(archive)}")
        moa = 0.2 + count * ((1 - 0.2) / iterations)
        mop = 1 - ((count ** (1 / alpha)) / (iterations ** (1 / alpha)))
        population = update_population(population, archive, grid, mu, moa, mop, problem)
        # Merge and sort solutions
        archive = non_dominated_sort(np.vstack((archive, population))) 
        # If the archive is compLeted
        if len(archive) > size:
            # Keep archive size manageable
            archive = archive[:size]  
        # If any of the newLy added answers to the archive is pLaced outside of the hypercubes
        if np.any([np.any(sol[-2:] < grid.min(axis=1)) or np.any(sol[-2:] >= grid.max(axis=1)) for sol in archive]):
            # Update the grids
            grid = compute_grid(archive[:, -2:], n_bins)
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
    dataset = RandomDataset(n_machines=5, n_tasks=10)
    dataset.plot()
    archive = run_moaoa(problem=dataset, iterations=100, verbose=True)
    print(archive)
    print(f'Archive Size: {len(archive)}')
    plot_pareto_front(archive)
    dataset.plot_schedule()
