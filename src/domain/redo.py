from dataclasses import dataclass


@dataclass
class RedoOperation:
    """
    Data class for redo operation object
    """
    object_service: object
    handler: object
    parameters: tuple
