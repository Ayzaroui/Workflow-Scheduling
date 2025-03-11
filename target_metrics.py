
import numpy as np

# get the cost of executing a task on a machine
def f_cost(dataset, solution):
    """Cost target function.
    Args: 
        dataset: dataset object
        solution: binary array of shape (n_tasks, n_machines)
    Returns: total cost of the solution    
    """
    cost = 0
    for i, task in enumerate(dataset.tasks):
        for j, machine in enumerate(dataset.machines):
            if solution[i, j] == 1:
                cost += machine.exec_cost(task) + machine.comm_cost(task)
    
    return cost

# get start and end time of a task
def get_end_time(dataset, task, machine):
    parent = dataset.get_task_by_id(task.parent_id)
    if task.id == 0:
        start_time = 0
    else:
        if not parent.is_done:
            return np.inf
        start_time = max(parent.end_time + task.input_size / parent.is_assigned.bandwidth)
    end_time = start_time + task.n_instructions / machine.cpu_mips
    return end_time

def f_makespan(dataset, solution):
    """Makespan target function.
    Args:
        dataset: dataset object
        solution: binary array of shape (n_tasks, n_machines)
    Returns: makespan of the solution
    """
    makespan = 0
    for i, task in enumerate(dataset.tasks):
        for j, machine in enumerate(dataset.machines):
            if solution[i, j] == 1:
                end_time = get_end_time(task, machine)
                makespan = max(makespan, end_time)
    return makespan

def check_feasibility(dataset, solution):
    """Check if the solution is feasible.
    Args:
        dataset: dataset object
        solution: binary array of shape (n_tasks, n_machines)
    Returns: True if the solution is feasible, False otherwise
    """
    # each task is assigned to exactly one machine
    if not np.all(np.sum(solution, axis=1) == 1):
        return False
    # # each machine can execute one task at a time
    # if ???:
    #     return False
    # # a task can only be executed if its predecessors are completed
    # if ???:
    #     return False
    return True

def compute_metrics(dataset, solution):
    """Schedule tasks on machines.
    Args:
        solution: binary array of shape (n_tasks, n_machines)
    Returns: (makespan, cost): QoS metrics
    """
    # Check dimensions
    if solution.shape != (dataset.n_tasks, dataset.n_machines):
        raise ValueError("Invalid solution shape")
    # Check feasibility
    if not check_feasibility(dataset, solution):
        return np.inf, np.inf
    # Compute QoS metrics
    makespan = f_makespan(dataset, solution)
    cost = f_cost(dataset, solution)

    return makespan, cost