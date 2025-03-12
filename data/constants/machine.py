class Machine(object):

    def __init__(self, id, cpu_cost, cpu_mips, is_cloud):
    
        """
        id: int -> Identifiant unique de la tâche.
        cpu_cost: float -> Coût d'utilisation du CPU (par heure ou par unité de temps).
        cpu_mips: int -> Performance du CPU en MIPS (Million Instructions Per Second).
        is_cloud: bool -> Indique si la machine est une machine cloud (True) ou locale (False).
        end_time: float -> Temps de fin d'utilisation de la machine (initialisé à 0).
        """
        
        # Constants
        self.id = id
        self.cpu_cost = cpu_cost
        self.cpu_mips = cpu_mips
        self.is_cloud = is_cloud
        # Variables
        self.end_time = 0

    def __str__(self):
        return f"Machine {self.id}:\n"\
            f"cpu_cost: {self.cpu_cost}\n"\
            f"cpu_mips: {self.cpu_mips}\n"\
            f"is_cloud: {self.is_cloud}\n"\
            f"end_time: {self.end_time}\n"
    