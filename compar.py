import numpy as np
import matplotlib.pyplot as plt

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.termination import get_termination
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from data.dataset import Dataset
from target_metrics import compute_metrics
from maoa import moaoa


N_TASKS = 50
N_MACHINES = 5
POPULATION_SIZE = 50
GENERATIONS = 100
RUNS = 10

dataset = Dataset(n_machines=N_MACHINES, n_tasks=N_TASKS)

class WorkflowSchedulingProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=N_TASKS * N_MACHINES, 
                         n_obj=2, 
                         n_constr=0, 
                         xl=0, 
                         xu=1)

    def _evaluate(self, x, out, *args, **kwargs):
        solution_matrix = x.reshape((N_TASKS, N_MACHINES))
        solution_matrix = np.round(solution_matrix)
        for i in range(N_TASKS):
            if np.sum(solution_matrix[i]) != 1:
                solution_matrix[i] = np.zeros(N_MACHINES)
                solution_matrix[i, np.random.randint(0, N_MACHINES)] = 1
        makespan, cost = compute_metrics(dataset, solution_matrix)
        out["F"] = np.array([makespan, cost])


def run_nsga2():
    problem = WorkflowSchedulingProblem()
    algorithm = NSGA2(
        pop_size=POPULATION_SIZE,
        sampling=BinaryRandomSampling(),
        crossover=SBX(prob=0.9),
        mutation=PM(prob=0.1),
        eliminate_duplicates=True
    )
    res = minimize(problem,
                   algorithm,
                   termination=get_termination("n_gen", GENERATIONS),
                   seed=None,
                   verbose=False)
    return res.F


def run_moaoa():
    moaoa_res = moaoa(size=POPULATION_SIZE, n=N_TASKS, p=N_MACHINES, iterations=GENERATIONS, verbose=False)

    moaoa_res = np.asarray(moaoa_res)

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
    plt.scatter(nsga2_res[:, 0], nsga2_res[:, 1], label='NSGA-II', marker='o', color='blue', alpha=0.7)
    plt.plot(nsga2_res[:, 0], nsga2_res[:, 1], linestyle="dotted", color="blue", alpha=0.7)
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
        print(f"Run {run + 1}/{RUNS}")
        
        nsga2_result = run_nsga2()
        moaoa_result = run_moaoa()

        dom_moaoa, comparisons = compare_dominance(nsga2_result, moaoa_result)
        moaoa_wins += dom_moaoa
        total_comp += comparisons

        print(f"Run {run+1}: MOAOA domine NSGA-II dans {dom_moaoa} cas sur {comparisons} comparaisons.")
        plot_comparison(nsga2_result, moaoa_result)
    
    proportion = moaoa_wins / total_comp if total_comp > 0 else 0
    print(f"\nProportion de domination de MOAOA sur NSGA-II: {proportion:.2%}")

