from domain.undo import UndoOperation


class UndoException(Exception):
    """
    Exception class for undo
    """
    pass


class UndoService:
    """
    service class for undo operation
    """
    __undo_operations = []

    @staticmethod
    def store_operation(object_service, handler, *parameters):
        """
        Stores undo operations in list
        """
        UndoService.__undo_operations.append(UndoOperation(object_service, handler, parameters))

    @staticmethod
    def do_undo():
        """
        Checks if there are any undo operations and execute the undo
        """
        if len(UndoService.__undo_operations) == 0:
            raise UndoException("No more undo!")
        else:
            undo_operation = UndoService.__undo_operations.pop()
            undo_operation.handler(undo_operation.object_service, *undo_operation.parameters)
