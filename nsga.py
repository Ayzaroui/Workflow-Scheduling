import numpy as np
import matplotlib.pyplot as plt

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.termination import get_termination
from pymoo.operators.sampling.rnd import BinaryRandomSampling

from data.randomDataset import RandomDataset
from target_metrics import compute_metrics


class WorkflowSchedulingProblem(ElementwiseProblem):
    def __init__(self, problem):
        self.problem = problem
        self.n_tasks = problem.n_tasks
        self.n_machines = problem.n_machines
        super().__init__(n_var=self.n_tasks * self.n_machines, 
                         n_obj=2, 
                         n_constr=0, 
                         xl=0, 
                         xu=1)

    def _evaluate(self, x, out, *args, **kwargs):
        solution_matrix = x.reshape((self.n_tasks, self.n_machines))
        solution_matrix = np.round(solution_matrix)
        for i in range(self.n_tasks):
            if np.sum(solution_matrix[i]) != 1:
                solution_matrix[i] = np.zeros(self.n_machines)
                solution_matrix[i, np.random.randint(0, self.n_machines)] = 1
        makespan, cost = compute_metrics(self.problem, solution_matrix)
        out["F"] = np.array([makespan, cost])

def run_nsga2(problem, population_size, generations, verbose=True):
    problem = WorkflowSchedulingProblem(problem)
    algorithm = NSGA2(
        pop_size=population_size,
        sampling=BinaryRandomSampling(),
        crossover=SBX(prob=0.9),
        mutation=PM(prob=0.1),
        eliminate_duplicates=True
    )
    res = minimize(problem,
                   algorithm,
                   termination=get_termination("n_gen", generations),
                   seed=1,
                   verbose=verbose)
    return res.F

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
    nsga2_result = run_nsga2(dataset, 50, 100)
    print(nsga2_result)
    print(f'Archive Size: {len(nsga2_result)}')
    plot_pareto_front(nsga2_result)
    dataset.plot_schedule()
