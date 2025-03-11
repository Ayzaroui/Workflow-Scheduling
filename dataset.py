import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from data.constants.task import Task
from data.constants.machine import Machine

np.random.seed(random.randint(0, 2**12 - 1))  

# Paramètres
cloud_machines_params_range = {
    "bandwidth": (100, 10000), 
    "cpu_cost": (0.1, 10), 
    "cpu_mips": (5000, 100000), 
    "bandwidth_cost": (0.01, 0.5), 
}

fog_machines_params_range = {
    "bandwidth": (1, 1000), 
    "cpu_cost": (0.05, 1), 
    "cpu_mips": (1000, 50000), 
    "bandwidth_cost": (0.001, 0.05), 
}

task_params_range = {
    "n_instructions": (1, 10**6),
    "data_volume": (1, 5000),
}

# Fonctions
def generate_bandwidth(n_machines, is_cloud):
    machines_params_range = cloud_machines_params_range if is_cloud else fog_machines_params_range
    bandwidth = np.random.randint(machines_params_range["bandwidth"][0], machines_params_range["bandwidth"][1], size=(n_machines, n_machines))
    np.fill_diagonal(bandwidth, 0)
    return bandwidth

def generate_bandwidth_cost(n_machines, is_cloud):
    machines_params_range = cloud_machines_params_range if is_cloud else fog_machines_params_range
    bandwidth_cost = np.random.uniform(machines_params_range["bandwidth_cost"][0], machines_params_range["bandwidth_cost"][1], size=(n_machines, n_machines))
    np.fill_diagonal(bandwidth_cost, 0)
    return bandwidth_cost

def generer_parents(n_tasks, task_id):
    if task_id == 0:
        return []
    if task_id == 1:
        return [] if np.random.rand() < 0.5 else [0]
    taille = np.random.randint(0, task_id-1)  
    parents = np.random.randint(0, task_id-1, size=taille).tolist()
    return parents

def generate_data_volume(n_tasks):
    data_volume = np.random.randint(task_params_range["data_volume"][0], task_params_range["data_volume"][1], size=(n_tasks, n_tasks))
    np.fill_diagonal(data_volume, 0)
    return data_volume

def generate_machines(n_machines, is_cloud):
    machines = []
    for i in range(n_machines):
        machines_params_range = cloud_machines_params_range if is_cloud else fog_machines_params_range
        cpu_cost = np.random.uniform(machines_params_range["cpu_cost"][0], machines_params_range["cpu_cost"][1])
        cpu_mips = np.random.randint(machines_params_range["cpu_mips"][0], machines_params_range["cpu_mips"][1])
        machines.append(Machine(i, cpu_cost, cpu_mips, is_cloud))
    return machines

def generate_tasks_graph(n_tasks):
    tasks = []
    for i in range(n_tasks):
        parents_id = generer_parents(n_tasks, i)
        n_instructions = np.random.randint(task_params_range["n_instructions"][0], task_params_range["n_instructions"][1])
        tasks.append(Task(i, parents_id, n_instructions))
    return tasks

def plot_task_graph(tasks):
    G = nx.DiGraph()
    for task in tasks:
        G.add_node(task.id)
    for task in tasks:
        if task.parents_id:
            for parent in task.parents_id:
                G.add_edge(parent, task.id) 
    pos = nx.spring_layout(G, k=3, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, edge_color='gray')
    plt.title("Graphe des tâches")
    plt.show()


# Classe
class Dataset():
    def __init__(self, n_machines, n_tasks, is_cloud=True):
       
        self.n_machines = n_machines
        self.n_tasks = n_tasks

        self.machines = generate_machines(n_machines, is_cloud)
        self.tasks = generate_tasks_graph(n_tasks) 

        self.data_volume = generate_data_volume(n_tasks)

        self.bandwidth = generate_bandwidth(n_machines, is_cloud)
        self.bandwidth_cost = generate_bandwidth_cost(n_machines, is_cloud)

    def plot(self):
        return plot_task_graph(self.tasks)
    
    def get_task_by_id(self, task_id):
        return self.tasks[task_id]
    
    def get_machine_by_id(self, machine_id):
        return self.machines[machine_id]

# def get_available_machines(machines):
#     return [machine for machine in machines if machine.is_available]

# def exec_time(self, task, machine):
#     return task.n_instructions / machine.cpu_mips

# def bandwidth_time(self, task, machine):
#     return task.input_size / machine.bandwidth

# def total_time(self, task, machine):
#     return self.exec_time(task, machine) + self.bandwidth_time(task, machine)

# def exec_cost(self, task, machine):
#     return task.n_instructions * machine.cpu_cost

# def bandwidth_cost(self, task, machine):
#     return task.input_size * machine.bandwidth_cost

# def total_cost(self, task, machine):
#     return self.exec_cost(task, machine) + self.bandwidth_cost(task, machine)

# def get_undone_tasks(self, tasks):
#     return [task for task in tasks if not task.is_done]

# def get_unused_machines(self, machines):
#     return [machine for machine in machines if not machine.used_once]

# def affect_task(self, task, machines):
#     print("ID:", task.id)
#     parent_task = Task.get_task_by_id(tasks, task.parent_id)
#     if not parent_task.is_done and task.parent_id != 0:
#         print("Error! Parent task not done")
#         return None
#     available_machines = self.get_available_machines(machines)
#     for mach in available_machines:
#         print(mach.id, mach.is_available)
#     if not available_machines:
#         print("Error! No available machines")
#         return None
    
#     machine = available_machines[np.random.randint(0, len(available_machines))]
    
#     machine.is_available = False

#     task.is_assigned = machine.id
#     print(task.is_assigned)

#     available_machines.remove(machine)
#     print("Task assigned to machine", machine.id)
#     return task, machine, available_machines
    
# def execute_task(self, task, machine, machines):
#     print("ID:", task.id)
#     print("Machine:", task.is_assigned)
#     if task.is_assigned == -1:
#         print("Error! Task not assigned")
#         return None
#     task.is_executed = False
#     task.parent_done = True
#     print(task.is_assigned)
    
#     machine.used_once = True

#     machine.use_time += self.total_time(task, machine)
#     unused_machines = self.get_unused_machines(machines)

#     for mach in unused_machines:
#         mach.start_use += self.total_time(task, mach)

#     machine.is_available = True

#     task.is_done = True

#     return task, machine, unused_machines



# # Création du dataset avec 5 machines et 10 tâches
# dataset = Dataset(n_machines=5, n_tasks=10)
# print(dataset.get_machine_by_id(0))
# print(dataset.get_task_by_id(2))
# dataset.plot()



