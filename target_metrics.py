import numpy as np


def f_cost(dataset, solution):
    """ Fonction objectif de coût.
    Args: 
        dataset : objet dataset
            Ensemble de données contenant les informations sur les tâches et les machines.
        solution : tableau binaire de forme (n_tasks, n_machines)
            Matrice binaire indiquant l'affectation des tâches aux machines.
    Returns: 
            Coût total de la solution. 
    """
    def f_transfer_cost(dataset, task, machine):
        transfer_cost = 0
        pred_machines = [dataset.get_task_by_id(id).is_assigned for id in task.parents_id]
        for i in range(len(pred_machines)):
            if pred_machines[i] == machine.id:
                transfer_cost += 0
            else :
                transfer_cost += (dataset.data_volume[task.parents_id[i], task.id] / dataset.bandwidth[pred_machines[i], machine.id])*dataset.bandwidth_cost[pred_machines[i], machine.id]
        return transfer_cost
    
    cost = 0
    for task in dataset.tasks:
        for machine in dataset.machines:
            if solution[task.id, machine.id] == 1:
                # Execution cost
                exec_cost = (task.n_instructions / machine.cpu_mips) * machine.cpu_cost
                
                # Communication cost
                transfer_cost = f_transfer_cost(dataset,task,machine)
                
                # Update total cost
                cost += exec_cost + transfer_cost  
    return cost
    


def f_makespan(dataset, solution):
    """Makespan target function.
    Args:
        dataset : objet dataset
            Ensemble de données contenant les informations sur les tâches et les machines.
        solution : tableau binaire de forme (n_tasks, n_machines)
            Matrice binaire indiquant l'affectation des tâches aux machines.
    Returns: 
        Makespan de la solution.
    """
    makespan = 0
    for task in dataset.tasks:
        for machine in dataset.machines:
            if solution[task.id, machine.id] == 1:
                makespan = max(makespan, task.end_time)
    return makespan


def schedule(dataset, solution):
    """Planifie les tâches sur les machines.
    Args:
        dataset : objet dataset
            Contient les informations sur les tâches et les machines.
        solution : tableau binaire de forme (n_tasks, n_machines)
            Matrice binaire indiquant l'affectation des tâches aux machines.
    Returns:
        0
    """
    # Schedule tasks
    for task in dataset.tasks:
        for machine in dataset.machines:
            if solution[task.id, machine.id] == 1:
                execute_task(dataset, task, machine)
    return 0

def execute_task(dataset, task, machine):
    """Exécute une tâche sur une machine.
    Args:
        dataset : objet dataset
            Contient les informations sur les tâches et les machines.
        task : objet tâche
            La tâche à exécuter.
        machine : objet machine
            La machine sur laquelle exécuter la tâche.
    Returns:
        0
    """

    def get_start_time(dataset, task, machine):

        predecessors = [dataset.get_task_by_id(id) for id in task.parents_id]
        pred_machines = [p.is_assigned for p in predecessors]
        end_times = [p.end_time for p in predecessors]

        bandwidths = [dataset.bandwidth[id, machine.id] for id in pred_machines]
        data_volumes = [dataset.data_volume[p, task.id] for p in task.parents_id]

        # get end time of predecessors
        pred_end = 0
        for i in range(len(predecessors)):
            if bandwidths[i] == 0:
                transfer_time = 0
            else:
                transfer_time = data_volumes[i] / bandwidths[i]
            pred_end = max(pred_end, end_times[i] + transfer_time)

        # get start time
        start_time = max(pred_end, machine.end_time)
        return start_time


    # assign task to machine
    task.is_assigned = machine.id

    # get start and end time
    start_time = get_start_time(dataset, task, machine)
    end_time = start_time + task.n_instructions / machine.cpu_mips
    
    # update task and machine end time
    task.start_time = start_time
    task.end_time = end_time
    machine.end_time = end_time
    return 0

def compute_metrics(dataset, solution):
    """Planifie les tâches sur les machines et calcule les métriques de QoS.
    Args:
        dataset : objet dataset
            Contient les informations sur les tâches et les machines.
        solution : tableau binaire de forme (n_tasks, n_machines)
            Matrice binaire indiquant l'affectation des tâches aux machines.
    Returns:
        Métriques de Qualité de Service (QoS).
    """
    def check_constraint(solution):
        # each task is assigned to exactly one machine
        if not np.all(np.sum(solution, axis=1) == 1):
            print("Error! Each task must be assigned to exactly one machine")
            return False
        return True
    
    # Check dimensions
    if solution.shape != (dataset.n_tasks, dataset.n_machines):
        raise ValueError("Invalid solution shape")
    
    # Check feasibility
    if not check_constraint(solution):
        return np.inf, np.inf
    
    # Schedule tasks
    schedule(dataset, solution)

    # Compute QoS metrics
    makespan = f_makespan(dataset, solution)
    cost = f_cost(dataset, solution)
    return makespan, cost


if __name__ == '__main__':
    # Test functions
    from data.dataset import Dataset
    dataset = Dataset(n_machines=5, n_tasks=7)
    solution = np.zeros((dataset.n_tasks, dataset.n_machines))

    for line in solution:
        line[np.random.randint(0, dataset.n_machines)] = 1

    makespan, cost = compute_metrics(dataset, solution)
    print("Solution:", solution)
    print("Makespan:", makespan)
    print("Cost:", cost)

    for task in dataset.tasks:
        print(task)
    for machine in dataset.machines:
        print(machine)

    dataset.plot()