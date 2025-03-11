class Task(object):

    def __init__(self, id, parents_id, n_instructions, is_assigned=-1, parent_done=False, is_done=False):
        
        self.id = id
        self.parents_id = parents_id
        self.n_instructions = n_instructions
        self.is_assigned = is_assigned
        self.is_done = is_done
        self.start_time = 0
        self.end_time = 0

    """
    parent_id: int -> ID de la tâche parente
    n_instructions: int -> Nombre d'instructions
    is_assigned: int -> Machine à laquelle la task est affectée (-1 sinon)
    """
    def __str__(self):
        return f"Task {self.id}:\n"\
            f"parents_id: {self.parents_id}\n"\
            f"n_instructions: {self.n_instructions}\n"\
            f"is_assigned: {self.is_assigned}\n"\
            f"is_done: {self.is_done}\n"
