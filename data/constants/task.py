class Task(object):

    def __init__(self, id, parents_id, n_instructions):

        """
        id: int -> Identifiant unique de la tâche.
        parent_id: int -> Liste des identifiants des tâches parentes dont cette tâche dépend.
        n_instructions: int -> Nombre d'instructions à exécuter pour cette tâche.
        is_assigned: int -> Identifiant de la machine à laquelle la tâche est affectée (-1 si elle n'est pas encore assignée).
        start_time: float -> Temps de début d'exécution de la tâche (initialisé à 0).
        end_time: float -> Temps de fin d'exécution de la tâche (initialisé à 0).
        """
        
        # Constants
        self.id = id
        self.parents_id = parents_id
        self.n_instructions = n_instructions
        # Variables
        self.is_assigned = None
        self.start_time = None
        self.end_time = None

    def __str__(self):
        return f"Task {self.id}:\n"\
            f"parents_id: {self.parents_id}\n"\
            f"n_instructions: {self.n_instructions}\n"\
            f"is_assigned: {self.is_assigned}\n"\
            f"self.start_time: {self.start_time}\n"\
            f"self.end_time: {self.end_time}\n"