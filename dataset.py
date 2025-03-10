from data.constants.machine import Machine
from data.constants.task import Task
import numpy as np
class Dataset():
    def __init__(self, n_machines, n_tasks):
        self.n_machines = n_machines
        self.n_tasks = n_tasks

    machines_params_range = {
    "bandwidth": (10, 10000),  # Bande passante en Mbps, peut aller de quelques Mbps (réseaux locaux) à des milliers de Mbps pour des serveurs dédiés ou cloud.
    "ram": (2, 512),  # Mémoire RAM en Go, typiquement entre 2 Go (pour des systèmes légers) et 512 Go pour des serveurs haute performance.
    "ram_cost": (0.01, 0.5),  # Coût par Go de RAM par heure ou par unité, en fonction des services cloud (ex. AWS, Azure, Google Cloud).
    "n_cpus": (1, 64),  # Nombre de CPU, de 1 à 64, qui est typique dans les serveurs ou machines dédiées.
    "cpu_cost": (0.05, 5),  # Coût par CPU par heure ou par unité, en fonction de la puissance de calcul (ex. AWS, Google Cloud).
    "cpu_mips": (1000, 100000),  # Millions d'instructions par seconde (MIPS), typiquement entre 1000 et 100000 pour des processeurs modernes.
    "bandwidth_cost": (0.001, 0.1),  # Coût de la bande passante par Go ou Mo, peut varier en fonction des services cloud et du type de réseau.
    "distance": (0, 5000),  # Distance en kilomètres, pour simuler les différences de latence et de coût de transmission dans un environnement de cloud/fog.
}
    
    def generate_machines(self, n_machines, machines_params_range):
        machines = []
        for i in range(n_machines):
            bandwidth = np.random.randint(machines_params_range["bandwidth"][0], machines_params_range["bandwidth"][1])
            ram = np.random.randint(machines_params_range["ram"][0], machines_params_range["ram"][1])
            ram_cost = np.random.uniform(machines_params_range["ram_cost"][0], machines_params_range["ram_cost"][1])
            n_cpus = np.random.randint(machines_params_range["n_cpus"][0], machines_params_range["n_cpus"][1])
            cpu_cost = np.random.uniform(machines_params_range["cpu_cost"][0], machines_params_range["cpu_cost"][1])
            cpu_mips = np.random.randint(machines_params_range["cpu_mips"][0], machines_params_range["cpu_mips"][1])
            bandwidth_cost = np.random.uniform(machines_params_range["bandwidth_cost"][0], machines_params_range["bandwidth_cost"][1])
            distance = np.random.randint(machines_params_range["distance"][0], machines_params_range["distance"][1])
            is_cloud = np.random.choice([True, False])
            machines.append(Machine(bandwidth, ram, ram_cost, n_cpus, cpu_cost, cpu_mips, bandwidth_cost, is_cloud, distance))
        return machines
