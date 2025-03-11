class Task(object):
    _id_counter = 0  # Variable de classe pour suivre l'ID des tâches

    def __init__(self, parent_id, required_ram, n_instructions, input_size, output_size, is_assigned=-1, parent_done=False, is_done=False):
        self.id = Task._id_counter  # Assigne un ID unique
        Task._id_counter += 1  # Incrémente le compteur global

        self.parent_id = parent_id
        self.n_instructions = n_instructions
        self.input_size = input_size
        self.output_size = output_size
        self.is_assigned = is_assigned
        self.parent_done = parent_done
        self.is_done = is_done

    """
    parent_id: int -> ID de la tâche parente
    parallelism: int -> Pourcentage de parallélisme
    required_ram: int -> RAM requise
    n_instructions: int -> Nombre d'instructions
    input_size: int -> Taille des données d'entrée
    output_size: int -> Taille des données de sortie
    is_assigned: int -> Machine à laquelle la task est affectée (-1 sinon)
    """
    def get_task_by_id(self, tasks, task_id):
        for task in tasks:
            if task.id == task_id:
                return task
            
    def get_children(self, tasks):
        return [task for task in tasks if task.parent_id == self.id and task.id != self.id]
