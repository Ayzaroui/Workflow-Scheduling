class Machine(object):
    def __init__(self, bandwidth, ram, ram_cost, n_cpus, cpu_cost, cpu_mips, bandwidth_cost, is_cloud, distance, is_available=True):
        """
        bandwidth: int -> bandwidth in Mbps
        ram: int -> RAM in Go
        ram_cost: float -> RAM cost per hour or per unit
        n_cpus: int -> number of CPUs
        cpu_cost: float -> CPU cost per hour or per unit
        cpu_mips: int -> CPU MIPS
        bandwidth_cost: float -> bandwidth cost per Go or per Mbps
        distance: int -> distance in km
        is_cloud: bool -> whether the machine is in the cloud or not
        is_available: bool -> whether the machine is available or not
        """
        
        self.bandwidth = bandwidth
        self.ram = ram
        self.ram_cost = ram_cost
        self.n_cpus = n_cpus
        self.cpu_cost = cpu_cost
        self.cpu_mips = cpu_mips
        self.bandwidth_cost = bandwidth_cost
        self.distance = distance
        self.is_cloud = is_cloud
        self.is_available = is_available
    
    def generate_exec_cost(self):
        return self.ram_cost * self.ram + self.cpu_cost * self.n_cpus
    