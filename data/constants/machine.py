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
        cpu_cost: float -> CPU cost per hour or per unit
        cpu_mips: int -> CPU MIPS
        is_cloud: bool -> whether the machine is in the cloud or not
        is_available: bool -> whether the machine is available or not
        start_use: float -> start use time in seconds
        use_time: float -> use time in seconds
        used_once: bool -> whether the machine has been used once or not
        """

    def __str__(self):
        return f"Machine {self.id}:\n"\
            f"cpu_cost: {self.cpu_cost}\n"\
            f"cpu_mips: {self.cpu_mips}\n"\
            f"is_cloud: {self.is_cloud}\n"\
            f"is_available: {self.is_available}\n"\
            f"start_use: {self.start_use}\n"\
            f"use_time: {self.use_time}\n"\
            f"used_once: {self.used_once}\n"
    