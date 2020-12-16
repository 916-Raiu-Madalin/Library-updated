from dataclasses import dataclass


@dataclass
class UndoOperation:
    """
    Data class for undo operation object
    """
    object_service: object
    handler: object
    parameters: tuple
