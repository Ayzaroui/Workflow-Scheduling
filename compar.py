import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from data.randomDataset import RandomDataset
from maoa import run_moaoa
from nsga import run_nsga2


POPULATION_SIZE = 50
GENERATIONS = 100
RUNS = 10
N_MACHINES = 7
N_TASKS = 12


def check_moaoa(archive):
    moaoa_res = np.asarray(archive)

    if moaoa_res.shape[1] < 2:
        raise ValueError(f"MOAOA ne retourne pas assez de colonnes, reçu: {moaoa_res.shape}")

    moaoa_res = moaoa_res[:, -2:]

    return moaoa_res



def compare_dominance(nsga2_res, moaoa_res):
    nsga2_res = np.asarray(nsga2_res)
    moaoa_res = np.asarray(moaoa_res)

    if nsga2_res.shape[1] != 2 or moaoa_res.shape[1] != 2:
        raise ValueError(f"Les solutions doivent avoir 2 colonnes (objectifs), "
                         f"mais nsga2_res.shape={nsga2_res.shape}, moaoa_res.shape={moaoa_res.shape}")

    moaoa_expanded = moaoa_res[:, np.newaxis, :] 
    nsga2_expanded = nsga2_res[np.newaxis, :, :]

    domination_matrix = (moaoa_expanded[:, :, 0] < nsga2_expanded[:, :, 0]) & \
                        (moaoa_expanded[:, :, 1] < nsga2_expanded[:, :, 1])

    moaoa_dominates = np.sum(domination_matrix)
    total_comparisons = moaoa_res.shape[0] * nsga2_res.shape[0]

    return moaoa_dominates, total_comparisons



def plot_comparison(nsga2_res, moaoa_res):
    nsga2_res = nsga2_res[np.argsort(nsga2_res[:, -2])]
    plt.scatter(nsga2_res[:, 0], nsga2_res[:, 1], label='NSGA-II', marker='o', color='blue', alpha=0.7)
    plt.plot(nsga2_res[:, 0], nsga2_res[:, 1], linestyle="dotted", color="blue", alpha=0.7)
    moaoa_res = moaoa_res[np.argsort(moaoa_res[:, -2])]
    plt.scatter(moaoa_res[:, -2], moaoa_res[:, -1], label='MOAOA', marker='s', color='red', alpha=0.7)
    plt.plot(moaoa_res[:, -2], moaoa_res[:, -1], linestyle="dotted", color="red", alpha=0.7)

    plt.xlabel('Makespan')
    plt.ylabel('Cost')
    plt.title('Comparison: NSGA-II vs MOAOA')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    moaoa_wins = 0
    total_comp = 0

    for run in range(RUNS):
        dataset = RandomDataset(n_machines=N_MACHINES, n_tasks=N_TASKS)
        print(f"Run {run + 1}/{RUNS}")
        
        _, nsga2_result = run_nsga2(dataset, POPULATION_SIZE, GENERATIONS)
        dataset.reset_schedule()
        moaoa_result = run_moaoa(problem=dataset, size=POPULATION_SIZE, iterations=GENERATIONS)
        moaoa_result = check_moaoa(moaoa_result)

        dom_moaoa, comparisons = compare_dominance(nsga2_result, moaoa_result)
        moaoa_wins += dom_moaoa
        total_comp += comparisons

        print(f"Run {run+1}: MOAOA domine NSGA-II dans {dom_moaoa} cas sur {comparisons} comparaisons.")
        plot_comparison(nsga2_result, moaoa_result)
    
    proportion = moaoa_wins / total_comp if total_comp > 0 else 0
    print(f"\nProportion de domination de MOAOA sur NSGA-II: {proportion:.2%}")

