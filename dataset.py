from data.constants.machine import Machine
from data.constants.task import Task
import numpy as np
class Dataset():
    def __init__(self, n_machines, n_tasks):
        self.n_machines = n_machines
        self.n_tasks = n_tasks

    cloud_machines_params_range = {
        "bandwidth": (0.1, 10),  # Bande passante en Gbps, de 100 Mbps pour des services cloud basiques à 10 Gbps.
        "ram": (8, 512),  # Mémoire RAM en Go, de 8 Go pour des machines basiques à 512 Go pour des serveurs haut de gamme.
        "ram_cost": (0.05, 1),  # Coût par Go de RAM, typiquement entre 0.05 et 1 $/Go/heure, en fonction des services cloud.
        "n_cpus": (2, 128),  # Nombre de CPU, de 2 à 128 cœurs pour des machines virtuelles ou serveurs dédiés dans le cloud.
        "cpu_cost": (0.1, 10),  # Coût par CPU, typiquement de 0.1 à 10 $/CPU/heure selon la puissance et la taille du serveur.
        "cpu_mips": (5000, 100000),  # MIPS (Millions d'Instructions par Seconde), de 5000 MIPS à 100000 MIPS pour des processeurs modernes dans le cloud.
        "bandwidth_cost": (0.01, 0.5),  # Coût de la bande passante par Go, généralement de 0.01 à 0.5 $/Go selon le fournisseur de cloud.
        "distance": (500, 10000),  # Distance en kilomètres, simule la latence entre les utilisateurs et les datacenters distants.
    }

    fog_machines_params_range = {
        "bandwidth": (0.001, 1),  # Bande passante en Gbps, généralement entre 1 Mbps pour les appareils IoT jusqu'à 1 Gbps pour des passerelles locales.
        "ram": (2, 64),  # Mémoire RAM en Go, de 2 Go pour des dispositifs IoT de base à 64 Go pour des passerelles ou serveurs fog.
        "ram_cost": (0.01, 0.2),  # Coût de la RAM, généralement entre 0.01 et 0.2 $/Go/heure pour des dispositifs fog moins chers.
        "n_cpus": (1, 16),  # Nombre de CPU, généralement entre 1 et 16 pour les dispositifs fog ou petites passerelles locales.
        "cpu_cost": (0.05, 1),  # Coût par CPU, souvent entre 0.05 et 1 $/CPU/heure pour des ressources locales ou IoT.
        "cpu_mips": (1000, 50000),  # MIPS pour les processeurs dans les dispositifs fog, de 1000 MIPS à 50000 MIPS pour des processeurs embarqués.
        "bandwidth_cost": (0.001, 0.05),  # Coût de la bande passante, généralement entre 0.001 et 0.05 $/Go dans le fog.
        "distance": (0, 1000),  # Distance en kilomètres, généralement plus proche de l'utilisateur final, donc avec moins de latence.
    }

    
    def generate_machines(self, n_machines, fog_machines_params_range, cloud_machines_params_range):
        machines = []
        for i in range(n_machines):
            is_cloud = np.random.choice([True, False])
            machines_params_range = cloud_machines_params_range if is_cloud else fog_machines_params_range
            bandwidth = np.random.randint(machines_params_range["bandwidth"][0], machines_params_range["bandwidth"][1])
            ram = np.random.randint(machines_params_range["ram"][0], machines_params_range["ram"][1])
            ram_cost = np.random.uniform(machines_params_range["ram_cost"][0], machines_params_range["ram_cost"][1])
            n_cpus = np.random.randint(machines_params_range["n_cpus"][0], machines_params_range["n_cpus"][1])
            cpu_cost = np.random.uniform(machines_params_range["cpu_cost"][0], machines_params_range["cpu_cost"][1])
            cpu_mips = np.random.randint(machines_params_range["cpu_mips"][0], machines_params_range["cpu_mips"][1])
            bandwidth_cost = np.random.uniform(machines_params_range["bandwidth_cost"][0], machines_params_range["bandwidth_cost"][1])
            distance = np.random.randint(machines_params_range["distance"][0], machines_params_range["distance"][1])
            machines.append(Machine(bandwidth, ram, ram_cost, n_cpus, cpu_cost, cpu_mips, bandwidth_cost, is_cloud, distance))
        return machines
    
    task_params_range = {
    "parallelism": (0, 100),  # Pourcentage de parallélisme (0 = séquentiel, 100 = totalement parallélisable)
    "required_ram": (1, 256),  # RAM requise en Go
    "n_instructions": (10**6, 10**12),  # Nombre d'instructions
    "input_size": (1, 5000),  # Taille des données d'entrée en Mo
    "output_size": (1, 5000),  # Taille des données de sortie en Mo
    "is_assigned": [True, False]  # Si la tâche est assignée ou non
}
    
    def generate_tasks(self, n_tasks, task_params_range):
        tasks = []
        for i in range(n_tasks):
            parallelism = np.random.randint(task_params_range["parallelism"][0], task_params_range["parallelism"][1])
            required_ram = np.random.randint(task_params_range["required_ram"][0], task_params_range["required_ram"][1])
            n_instructions = np.random.randint(task_params_range["n_instructions"][0], task_params_range["n_instructions"][1])
            input_size = np.random.randint(task_params_range["input_size"][0], task_params_range["input_size"][1])
            output_size = np.random.randint(task_params_range["output_size"][0], task_params_range["output_size"][1])
            tasks.append(Task(parallelism, required_ram, n_instructions, input_size, output_size))
        return tasks
