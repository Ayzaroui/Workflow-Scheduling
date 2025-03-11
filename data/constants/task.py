class Task(object):
    _id_counter = 0  # Variable de classe pour suivre l'ID des tâches

    def __init__(self, id, parents_id, n_instructions, is_assigned=-1, parent_done=False, is_done=False):
        
        self.id = id
        self.parent_id = parents_id
        self.n_instructions = n_instructions
        self.is_assigned = is_assigned
        self.is_done = is_done

    """
    parent_id: int -> ID de la tâche parente
    n_instructions: int -> Nombre d'instructions
    is_assigned: int -> Machine à laquelle la task est affectée (-1 sinon)
    """
