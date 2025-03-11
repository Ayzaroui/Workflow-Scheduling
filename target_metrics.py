
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
    for task in dataset.tasks:
        for machine in dataset.machines:
            if solution[task.id, machine.id] == 1:
                # Execution cost
                exec_cost = task.n_instructions / machine.cpu_mips * machine.cpu_cost
                # Communication cost
                predecessors = [dataset.get_task_by_id(id) for id in task.parents_id]
                pred_machines = [p.is_assigned for p in predecessors]
                transfer_cost = sum([dataset.bandwidth_cost[id, machine.id] for id in pred_machines])
                # Update total cost
                cost += exec_cost + transfer_cost
    
    return cost

def f_makespan(dataset, solution):
    """Makespan target function.
    Args:
        dataset: dataset object
        solution: binary array of shape (n_tasks, n_machines)
    Returns: makespan of the solution
    """
    makespan = 0
    for task in dataset.tasks:
        for machine in dataset.machines:
            if solution[task.id, machine.id] == 1:
                makespan = max(makespan, task.end_time)
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
        print("Error! Each task must be assigned to exactly one machine")
        return False
    # # each machine can execute one task at a time
    # if ???:
    #     return False
    # # a task can only be executed if its predecessors are completed
    # if ???:
    #     return False
    return True

def schedule(dataset, solution):
    """Schedule tasks on machines.
    Args:
        dataset: dataset object
        solution: binary array of shape (n_tasks, n_machines)
    Returns: schedule: list of tuples (task_id, machine_id, start_time, end_time)
    """
    # Check dimensions
    if solution.shape != (dataset.n_tasks, dataset.n_machines):
        raise ValueError("Invalid solution shape")
    # Schedule tasks
    for task in dataset.tasks:
        for machine in dataset.machines:
            if solution[task.id, machine.id] == 1:
                execute_task(dataset, task, machine)

def execute_task(dataset, task, machine):
    """Assign a task to a machine.
    Args:
        task: task object
        machine: machine object
    """
    # assign task to machine
    task.is_assigned = machine.id
    # get predecessors
    predecessors = [dataset.get_task_by_id(id) for id in task.parents_id]
    # get communication time
    pred_machines = [p.is_assigned for p in predecessors]
    bandwidths = [dataset.bandwidth[id, machine.id] for id in pred_machines]
    data_volumes = [dataset.data_volume[p, task.id] for p in task.parents_id]
    end_times = [p.end_time for p in predecessors]
    # get end time of predecessors
    pred_end = 0
    for i in range(len(predecessors)):
        if bandwidths[i] == 0:
            transfer_time = 0
        else:
            transfer_time = data_volumes[i] / bandwidths[i]
        pred_end = max(pred_end, end_times[i] + transfer_time)
    # get start
    start_time = max(pred_end, machine.end_time)
    # get end time
    end_time = start_time + task.n_instructions / machine.cpu_mips
    # update task and machine end time
    task.is_done = True # TODO: is this necessary?
    task.start_time = start_time
    task.end_time = end_time
    machine.end_time = end_time

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
    # Schedule tasks
    schedule(dataset, solution)
    # Compute QoS metrics
    makespan = f_makespan(dataset, solution)
    cost = f_cost(dataset, solution)

    return makespan, cost


# from dataset import Dataset
# # test the functions with mock solution
# dataset = Dataset(n_machines=5, n_tasks=10)
# solution = np.zeros((dataset.n_tasks, dataset.n_machines))
# # make sure the solution is feasible
# for line in solution:
#     line[np.random.randint(0, dataset.n_machines)] = 1
# print(solution)
# makespan, cost = compute_metrics(dataset, solution)
# print("Makespan:", makespan)
# print("Cost:", cost)
