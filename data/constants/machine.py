class Machine(object):

    def __init__(self, id, cpu_cost, cpu_mips, is_cloud, is_available=True, start_use=0.0, use_time=0.0, used_once=False):
        
        self.id = id
        self.cpu_cost = cpu_cost
        self.cpu_mips = cpu_mips
        self.is_cloud = is_cloud
        self.is_available = is_available
        self.start_use = start_use
        self.use_time = use_time
        self.used_once = used_once
        self.end_time = 0
    
        """
        id: int -> Identifiant unique de la tâche.
        cpu_cost: float -> Coût d'utilisation du CPU (par heure ou par unité de temps).
        cpu_mips: int -> Performance du CPU en MIPS (Million Instructions Per Second).
        is_cloud: bool -> Indique si la machine est une machine cloud (True) ou locale (False).
        is_available: bool -> Indique si la machine est disponible pour exécuter des tâches.
        start_use: float -> Temps de début d'utilisation de la machine en secondes.
        use_time: float -> Temps total d'utilisation de la machine en secondes.
        used_once: bool -> Indique si la machine a déjà été utilisée au moins une fois.
        end_time: float -> Temps de fin d'utilisation de la machine (initialisé à 0).
        """

    def __str__(self):
        return f"Machine {self.id}:\n"\
            f"cpu_cost: {self.cpu_cost}\n"\
            f"cpu_mips: {self.cpu_mips}\n"\
            f"is_cloud: {self.is_cloud}\n"\
            f"is_available: {self.is_available}\n"\
            f"start_use: {self.start_use}\n"\
            f"use_time: {self.use_time}\n"\
            f"used_once: {self.used_once}\n"\
            f"end_time: {self.end_time}\n"
    