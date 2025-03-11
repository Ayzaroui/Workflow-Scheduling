import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from data.constants.task import Task
from data.constants.machine import Machine
import random

class Dataset():
    def __init__(self, n_machines, n_tasks):
        # Initialiser la seed aléatoire pour garantir des résultats différents à chaque exécution
        random.seed()  # Utilise l'heure actuelle pour générer une seed aléatoire
        np.random.seed(random.randint(0, 2**12 - 1))  # Vous pouvez aussi définir votre propre valeur pour np.random.seed

        self.n_machines = n_machines
        self.n_tasks = n_tasks

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

    def generate_machines(self, n_machines, fog_machines_params_range, cloud_machines_params_range):
        machines = []
        for i in range(n_machines):
            is_cloud = np.random.choice([True, False])
            machines_params_range = cloud_machines_params_range if is_cloud else fog_machines_params_range
            bandwidth = np.random.randint(machines_params_range["bandwidth"][0], machines_params_range["bandwidth"][1])
            cpu_cost = np.random.uniform(machines_params_range["cpu_cost"][0], machines_params_range["cpu_cost"][1])
            cpu_mips = np.random.randint(machines_params_range["cpu_mips"][0], machines_params_range["cpu_mips"][1])
            bandwidth_cost = np.random.uniform(machines_params_range["bandwidth_cost"][0], machines_params_range["bandwidth_cost"][1])
            machines.append(Machine(bandwidth, cpu_cost, cpu_mips, bandwidth_cost, is_cloud))
        return machines

    task_params_range = {
        "n_instructions": (1, 10**6),
        "input_size": (1, 5000),
        "output_size": (1, 5000),
    }

    def generate_tasks_graph(self, n_tasks, task_params_range):
        tasks = []

        for i in range(n_tasks):
            parent_id = np.random.randint(0, i) if i > 0 else 0  # L'ID du parent est 0 pour le premier nœud
            n_instructions = np.random.randint(task_params_range["n_instructions"][0], task_params_range["n_instructions"][1])
            input_size = np.random.randint(task_params_range["input_size"][0], task_params_range["input_size"][1])
            output_size = np.random.randint(task_params_range["output_size"][0], task_params_range["output_size"][1])
            tasks.append(Task(parent_id, n_instructions, input_size, output_size))

        return tasks

    def plot_task_graph(self, tasks):
        G = nx.DiGraph()

        # Ajouter les nœuds avec des attributs
        for task in tasks:
            G.add_node(task.id)

        # Ajouter les arêtes en remplaçant None par 0 (Root) pour qu'il n'y ait pas de doublons
        for task in tasks:
            parent = task.parent_id  # Si parent_id est None, il sera remplacé par 0 lors de l'ajout des arêtes
            G.add_edge(parent, task.id)  # Ajout d'arêtes avec le parent_id correct

        # Générer la mise en page avec plus d'espacement
        pos = nx.spring_layout(G, k=2, seed=42)  # 🔥 Augmenter k pour espacer les nœuds

        # Dessiner le graphe
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, edge_color='gray')

        plt.title("Graphe des tâches avec espacement amélioré")
        plt.show()

    def get_available_machines(self, machines):
        return [machine for machine in machines if machine.is_available]

    def exec_time(self, task, machine):
        return task.n_instructions / machine.cpu_mips
    
    def bandwidth_time(self, task, machine):
        return task.input_size / machine.bandwidth
    
    def total_time(self, task, machine):
        return self.exec_time(task, machine) + self.bandwidth_time(task, machine)
    
    def exec_cost(self, task, machine):
        return task.n_instructions * machine.cpu_cost
    
    def bandwidth_cost(self, task, machine):
        return task.input_size * machine.bandwidth_cost
    
    def total_cost(self, task, machine):
        return self.exec_cost(task, machine) + self.bandwidth_cost(task, machine)

    def get_undone_tasks(self, tasks):
        return [task for task in tasks if not task.is_done]

    def get_unused_machines(self, machines):
        return [machine for machine in machines if not machine.used_once]

    def affect_task(self, task, machines):
        print("ID:", task.id)
        parent_task = Task.get_task_by_id(tasks, task.parent_id)
        if not parent_task.is_done and task.parent_id != 0:
            print("Error! Parent task not done")
            return None
        available_machines = self.get_available_machines(machines)
        for mach in available_machines:
            print(mach.id, mach.is_available)
        if not available_machines:
            print("Error! No available machines")
            return None
        
        machine = available_machines[np.random.randint(0, len(available_machines))]
        
        machine.is_available = False

        task.is_assigned = machine.id
        print(task.is_assigned)

        available_machines.remove(machine)
        print("Task assigned to machine", machine.id)
        return task, machine, available_machines
        
    def execute_task(self, task, machine, machines):
        print("ID:", task.id)
        print("Machine:", task.is_assigned)
        if task.is_assigned == -1:
            print("Error! Task not assigned")
            return None
        task.is_executed = False
        task.parent_done = True
        print(task.is_assigned)
        
        machine.used_once = True

        machine.use_time += self.total_time(task, machine)
        unused_machines = self.get_unused_machines(machines)

        for mach in unused_machines:
            mach.start_use += self.total_time(task, mach)

        machine.is_available = True

        task.is_done = True

        return task, machine, unused_machines
    
    # def execute_tasks(self, tasks, machines,start=False):
    #     if start:
    #         task = tasks[0]
    #     undone_tasks = self.get_undone_tasks(tasks)
    #     task, machine = self.affect_task(task, machines)
    #     children = task.get_children(undone_tasks)
    #     task, machine, unused_machines = self.execute_task(task, machines)
    #     for child in children:
    #         child, machine, unused_machines = self.execute_tasks(children, machines, start=False)
    #     return task, machine


# Création du dataset avec 5 machines et 10 tâches
dataset = Dataset(n_machines=5, n_tasks=10)

# Génération des machines et des tâches
machines = dataset.generate_machines(dataset.n_machines, dataset.fog_machines_params_range, dataset.cloud_machines_params_range)
tasks = dataset.generate_tasks_graph(dataset.n_tasks, dataset.task_params_range)

# Affichage des machines générées
print("Machines générées:")
for i, machine in enumerate(machines):
    print(f"Machine {i}: {vars(machine)}")

# Affichage des tâches générées
print("\nTâches générées:")
for i, task in enumerate(tasks):
    print(f"Tâche {i}: {vars(task)}")

dataset.plot_task_graph(tasks)

# Affectation des tâches aux machines
available_machines = dataset.get_available_machines(machines)
# for task in tasks:
#     result = dataset.affect_task(task, available_machines)
#     if result is None:
#         # Gérer le cas où la fonction retourne None
#         print("La tâche ne peut pas être affectée.")
#     else:
#         task, machine, available_machines = result

# Exécuter les tâches
task, machine, available_machines = dataset.affect_task(tasks[0], available_machines)
task, machine, unused_machines = dataset.execute_task(task, machine, machines)
print("Task executed:", task.id)

# dataset.execute_tasks(tasks, machines)
