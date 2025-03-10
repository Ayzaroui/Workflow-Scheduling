class Task(object):
    def __init__(self, id, parallelism, required_ram, n_instructions, input_size, output_size, is_assigned=False):
        self.id = id
        self.parallelism = parallelism
        self.required_ram = required_ram
        self.n_instructions = n_instructions
        self.input_size = input_size
        self.output_size = output_size
        self.is_assigned = is_assigned

        """
        id: int -> id of the task
        parallelism: int -> percentage of parallelism
        required_ram: int
        n_instructions: int -> number of instructions
        input_size: int
        output_size: int
        is_assigned: bool -> whether the task is assigned to a machine or not
        """
