from domain.entities import Client
from iterable.module_iterable_filter_sort import filter_entities, shell_sort


class ClientService:
    def __init__(self, client_repository, validator):
        self.__client_repository = client_repository
        self.__validator = validator

    def add_client(self, client_id, name):
        """
        This method adds a client
        :param client_id:
        :param name:
        """
        p = Client(client_id, name)
        self.__validator.validate_client(p)
        self.__client_repository.save(p)

    def remove_client(self, client_id):
        """
        This method removes the client from the given id
        :param book_id:
        :return:
        """
        self.__client_repository.remove(client_id)

    def print_clients(self):
        return self.__client_repository.print_all()

    def search_client_by_id(self, value):
        """
        This method finds all the clients with a similar or same id as the parameter
        :param value:
        :return: The list of clients
        """

        # cop = self.__client_repository.get_entities()
        # plist = []
        # for i in cop:
        #     if value in cop[i].id:
        #         plist.append(cop[i])
        def sort_criteria_id(entity1,entity2):
            return entity1.id < entity2.id


        def search_criteria_id(key):
            return value in key.id

        cop = self.get_entities()
        entities = list(cop.values())

        plist = filter_entities(entities, search_criteria_id)
        shell_sort(plist,sort_criteria_id)

        return plist

    def search_client_by_name(self, name):
        """
        This method finds all the clients that have a similar or the same name as the parameter
        :param name:
        :return: The list of clients
        """

        # cop = self.__client_repository.get_entities()
        # plist = []
        # for i in cop:
        #     if name.lower() in cop[i].name.lower():
        #         plist.append(cop[i])
        def sort_criteria_name(name1, name2):
            return name1.name < name2.name

        def search_criteria_name(key):
            return name.lower() in key.name.lower()

        cop = self.get_entities()
        entities = list(cop.values())

        plist = filter_entities(entities, search_criteria_name)
        shell_sort(plist, sort_criteria_name)

        return plist

    def get_entities(self):
        return self.__client_repository.get_entities()
