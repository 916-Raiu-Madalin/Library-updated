from domain.redo import RedoOperation


class RedoException(Exception):
    """
    Exception class for undo
    """
    pass


class RedoService:
    """
    service class for redo operation
    """
    __redo_operations = []
    @staticmethod
    def clear():
        RedoService.__redo_operations.clear()
    @staticmethod
    def store_operation(object, handler, *parameters):
        """
        Stores redo operations in list
        """
        RedoService.__redo_operations.append(RedoOperation(object, handler, parameters))

    @staticmethod
    def do_redo():
        """
        Checks if there are any redo operations and execute the redo
        """
        if len(RedoService.__redo_operations) == 0:
            raise RedoException("No more redo!")
        else:
            redo_operation = RedoService.__redo_operations.pop()
            redo_operation.handler(redo_operation.object_service, *redo_operation.parameters)
