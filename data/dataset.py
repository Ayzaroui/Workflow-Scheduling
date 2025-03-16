import os
import sys
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import pandas as pd

from constants.task import Task
from constants.machine import Machine

# Random Seed
random.seed()
np.random.seed(random.randint(0, 2**12 - 1))  

#####################################################
# Paramètres
#####################################################
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

#####################################################
# Fonctions
#####################################################
def generate_bandwidth(is_cloud):
    bandwidth = np.zeros((len(is_cloud), len(is_cloud)))
    for i in range(len(is_cloud)):
        for j in range(i+1,len(is_cloud)):
            params_range = cloud_machines_params_range if not (is_cloud[i] and is_cloud[j]) else fog_machines_params_range
            bandwidth[i, j] = np.random.randint(params_range["bandwidth"][0], params_range["bandwidth"][1])
            bandwidth[j, i] = bandwidth[i, j]
    return bandwidth

def generate_bandwidth_cost(is_cloud):
    bandwidth_cost = np.zeros((len(is_cloud), len(is_cloud)))
    for i in range(len(is_cloud)):
        for j in range(i+1,len(is_cloud)):
            params_range = cloud_machines_params_range if not (is_cloud[i] and is_cloud[j]) else fog_machines_params_range
            bandwidth_cost[i, j] = np.random.uniform(params_range["bandwidth_cost"][0], params_range["bandwidth_cost"][1])
            bandwidth_cost[j, i] = bandwidth_cost[i, j]
    return bandwidth_cost

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

def convert_id(id):
    return int(id.split("ID")[1])

def extract_parent_task(file, mapping):
    for key, value in mapping.items():
        if key == file:
            return value
    return None

#####################################################
# Classe
#####################################################
class Dataset():
    def __init__(self, workflow_path, environment_path):
       
        self.load_workflow(workflow_path)
        self.load_environment(environment_path)
        self.reset_schedule() # Initialize the schedule

        # bandwidth and bandwidth_cost are not provided in the datasets
        # we generate them randomly
        self.bandwidth = generate_bandwidth([machine.is_cloud for machine in self.machines])
        self.bandwidth_cost = generate_bandwidth_cost([machine.is_cloud for machine in self.machines])

    def plot(self):
        return plot_task_graph(self.tasks)
    
    def get_task_by_id(self, task_id):
        return self.tasks[task_id]
    
    def get_machine_by_id(self, machine_id):
        return self.machines[machine_id]
    
    def load_workflow(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        namespace = {"pegasus": "http://pegasus.isi.edu/schema/DAX"}

        self.tasks = []

        # Extract all tasks
        for job in root.findall("pegasus:job", namespace):
            # create a task
            # there is no workload in the xml file, it will be set in the load_environment function
            task_id = convert_id(job.get("id"))
            self.tasks.append(Task(id=task_id, parents_id=[], n_instructions=0))

        self.n_tasks = len(self.tasks)

        # Find predecessors of each task
        for child in root.findall("pegasus:child", namespace):
            parent_ids = [convert_id(parent.get("ref")) for parent in child.findall("pegasus:parent", namespace)]
            child_id = convert_id(child.get("ref"))
            task = self.get_task_by_id(child_id)
            task.parents_id = parent_ids

        self.data_volume = np.zeros((self.n_tasks, self.n_tasks))

        # Data volume
        # find which task outputs which file
        mapping = {}
        for job in root.findall("pegasus:job", namespace):
            for uses in job.findall("pegasus:uses", namespace):
                if uses.get("link") == "output":
                    task_id = convert_id(job.get("id"))
                    mapping[uses.get("file")] = task_id
        # find the data volume between tasks
        for job in root.findall("pegasus:job", namespace):
            for uses in job.findall("pegasus:uses", namespace):
                if uses.get("link") == "input":
                    parent_id = extract_parent_task(uses.get("file"), mapping)
                    if parent_id is None:
                        continue
                    child_id = convert_id(job.get("id"))
                    child_task = self.get_task_by_id(child_id)
                    if parent_id != child_id and parent_id not in child_task.parents_id:
                        child_task.parents_id.append(parent_id)
                    self.data_volume[parent_id, child_id] += int(uses.get("size"))

    def load_environment(self, path):
        xls = pd.ExcelFile(path)

        # Correct the workloads of the tasks
        df_tasks = pd.read_excel(xls, 'TaskDetails')
        assert len(df_tasks) >= self.n_tasks, f"Number of tasks is greater in the dataset ({self.n_tasks}) than in the xlsx file ({len(df_tasks)})"
        for i in range(self.n_tasks):
            task = df_tasks.loc[i]
            self.tasks[i].n_instructions = task["Number of instructions (109 instructions)"]
        
        self.machines = []

        # Extract the machines
        df_machines = pd.read_excel(xls, 'NodeDetails')
        for i in range(len(df_machines)):
            machine = df_machines.loc[i]
            # "Node1 to Node3 are Cloud Nodes and Node4 to Node13 are Fog Nodes."
            is_cloud = True if i<3 else False
            self.machines.append(Machine(id=i, is_cloud=is_cloud, cpu_cost=machine["CPU usage cost"], cpu_mips=machine["CPU rate (MIPS)"]))

        self.n_machines = len(self.machines)
        
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

#####################################################
# Main
#####################################################
if __name__ == '__main__':
    dataset = Dataset(
        workflow_path=r"data\real_dataset\Montage_100.xml",
        environment_path=r"data\real_dataset\task120.xlsx"
    )
    print(dataset.get_machine_by_id(0))
    print(dataset.get_task_by_id(2))
    dataset.plot()