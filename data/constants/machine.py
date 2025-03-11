class Machine(object):
    _id_counter = 0
    def __init__(self, bandwidth, cpu_cost, cpu_mips, bandwidth_cost, is_cloud, is_available=True, start_use=0.0, use_time=0.0, used_once=False):
        Machine._id_counter += 1

        self.bandwidth = bandwidth
        self.cpu_cost = cpu_cost
        self.cpu_mips = cpu_mips
        self.bandwidth_cost = bandwidth_cost
        self.is_cloud = is_cloud
        self.is_available = is_available
        self.start_use = start_use
        self.use_time = use_time
        self.used_once = used_once
    
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
        start_use: float -> start use time in seconds
        use_time: float -> use time in seconds
        used_once: bool -> whether the machine has been used once or not
        """
    