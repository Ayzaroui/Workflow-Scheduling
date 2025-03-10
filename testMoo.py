import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.spea2 import SPEA2
from pymoo.optimize import minimize
from pymoo.core.callback import Callback
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import Mutation


from prefect import flow, task


class MultiObjectiveProblem(Problem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=2, n_constr=0, xl=np.zeros(2), xu=np.ones(2))

    def _evaluate(self, x, out, *args, **kwargs):
        # Assuming x is the population of solutions (size: 100, 2)
        f1 = x[:, 0] * x[:, 1]
        f2 = (1 - x[:, 0]) * (1 - x[:, 1])

        # Ensure F has shape (100, 2)
        out["F"] = np.column_stack([f1, f2])


@task
def init_optimization():
    return MultiObjectiveProblem()


@task
def run_optimization(problem):
    algorithm = NSGA2(
        pop_size=100,
        sampling=FloatRandomSampling(),
        crossover=SBX(eta=15, prob=0.9, n_offsprings=2),
        mutation = Mutation(prob=0.1),
        eliminate_duplicates=True
    )

    # Si vous ne voulez pas utiliser de callback, vous pouvez passer None
    res = minimize(problem,
                   algorithm,
                   ("n_gen", 100),
                   seed=1,
                   verbose=True,
                   callback=Callback())  # ou supprimez cet argument complètement

    return res


@task
def analyze_results(results):
    print("Solutions found:")
    print(results.X)
    print("Objectives:")
    print(results.F)
    print("Constraints:")
    print(results.G)


@flow
def optimization_workflow():
    problem = init_optimization()
    results = run_optimization(problem)
    analyze_results(results)


optimization_workflow()
