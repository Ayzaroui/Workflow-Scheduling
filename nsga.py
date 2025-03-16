import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.termination import get_termination
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.core.repair import Repair

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from data.dataset import Dataset
from target_metrics import compute_metrics
from maoa import repair_solution


class WorkflowSchedulingProblem(ElementwiseProblem):
    def __init__(self, problem):
        self.problem = problem
        self.n_tasks = problem.n_tasks
        self.n_machines = problem.n_machines
        super().__init__(n_var=self.n_tasks * self.n_machines, 
                         n_obj=2, 
                         n_ieq_constr=0,
                         n_eq_constr=1,
                         xl=0, 
                         xu=1)

    def _evaluate(self, x, out, *args, **kwargs):
        # x is a array of boolean values, we need to convert it to a binary matrix
        solution_matrix = x.reshape((self.n_tasks, self.n_machines)).astype(int)
        makespan, cost = compute_metrics(self.problem, solution_matrix)
        # objectvive values: makespan and cost
        out["F"] = np.array([makespan, cost])
        # equality constraint: each task is assigned to exactly one machine
        out["H"] = np.sum(np.sum(solution_matrix, axis=1) - 1)

class OneMachinePerTask(Repair):
    def _do(self, problem, population, **kwargs):
        for i in range(population.shape[0]):
            max_idx = problem.n_tasks * problem.n_machines
            x = population[i, :max_idx].astype(int)
            population[i, :max_idx] = repair_solution(x, problem.n_tasks, problem.n_machines).astype(bool)
        return population

def run_nsga2(problem, population_size, generations, verbose=True):
    problem = WorkflowSchedulingProblem(problem)
    X = np.zeros((problem.n_tasks, problem.n_machines))
    for i in range(problem.n_tasks):
        X[i, np.random.randint(0, problem.n_machines)] = 1
    algorithm = NSGA2(
        pop_size=population_size,
        sampling=BinaryRandomSampling(),
        crossover=TwoPointCrossover(),
        mutation=BitflipMutation(),
        repair=OneMachinePerTask(),
        eliminate_duplicates=True
    )
    res = minimize(problem,
                   algorithm,
                   termination=get_termination("n_gen", generations),
                   seed=1,
                   verbose=verbose)
    return res.X, res.F

def plot_pareto_front(archive):
    archive = archive[np.argsort(archive[:, -2])]
    plt.scatter(archive[:, -2], archive[:, -1])
    plt.plot(archive[:, -2], archive[:, -1], linestyle="dotted", color="blue", alpha=0.7)
    plt.xlabel('Makespan')
    plt.ylabel('Cost')
    plt.title('Pareto Front')
    plt.show()

if __name__ == '__main__':
    dataset = Dataset(
        # workflow_path=os.path.join("data", "CyberShake_100.xml"),
        # workflow_path=os.path.join("data", "Epigenomics_100.xml"),
        # workflow_path=os.path.join("data", "Inspiral_100.xml"),
        workflow_path=os.path.join("data/real_dataset", "Montage_100.xml"),
        environment_path=os.path.join("data/real_dataset", "task120.xlsx")
    ) 
    dataset.plot()
    poppulation, nsga2_result = run_nsga2(dataset, 50, 100)
    print(nsga2_result)
    print(f'Archive Size: {len(nsga2_result)}')
    compute_metrics(dataset, poppulation[0].reshape((dataset.n_tasks, dataset.n_machines)))
    plot_pareto_front(nsga2_result)

