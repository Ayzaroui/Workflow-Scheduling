import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from data.constants.task import Task
from data.constants.machine import Machine

# Random Seed
random.seed()
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

def generer_parents(task_id):
    if task_id == 0:
        return []
    if task_id == 1:
        return [] if np.random.rand() < 0.5 else [0]
    taille = np.random.randint(0, task_id)  
    parents = np.random.randint(0, task_id, size=taille).tolist()
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
        parents_id = generer_parents(i)
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
class RandomDataset():
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
        
    def reset_schedule(self):
        for task in self.tasks:
            task.is_assigned = None
            task.start_time = None
            task.end_time = None
        for machine in self.machines:
            machine.end_time = 0

    def plot_schedule(self):
        _, gnt = plt.subplots()
        gnt.set_xlabel('Time')
        gnt.set_yticks([i for i in range(self.n_machines)])
        gnt.set_yticklabels([f"Machine {i}" for i in range(self.n_machines)])
        # color matches the task id
        cmap = plt.get_cmap('tab20')
        colors = [cmap(i) for i in range(self.n_tasks)]
        for task in self.tasks:
            machine = self.get_machine_by_id(task.is_assigned)
            gnt.broken_barh([(task.start_time, task.end_time - task.start_time)], (machine.id - 0.4, 0.8), facecolors=colors[task.id])
        # add legend
        handles = [plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(self.n_tasks)]
        plt.legend(handles, [f'Task {i}' for i in range(self.n_tasks)], title='Tasks')
        plt.title('Schedule')
        plt.show()

if __name__ == '__main__':
    # Création du dataset avec 5 machines et 10 tâches
    dataset = RandomDataset(n_machines=5, n_tasks=10)
    print(dataset.get_machine_by_id(0))
    print(dataset.get_task_by_id(2))
    dataset.plot()