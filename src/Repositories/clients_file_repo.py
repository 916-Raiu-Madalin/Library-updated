from domain.entities import Client
from src.Repositories.repository import Repository



class ClientsFileRepository(Repository):
    def __init__(self, file_name):
        super().__init__({})
        self.__file_name = file_name
        self.__load_data()

    def save(self, client):
        super().save(client)
        self.__save_to_file(self.get_entities().values())

    def __save_to_file(self, clients):
        with open(self.__file_name, "w") as f:
            try:
                for client in clients:
                    client_str = str(client.id) + ';' + str(client.name)
                    f.write(client_str + "\n")
            except Exception as e:
                raise Exception(e)

    def remove(self, entity_id):
        super().remove(entity_id)
        self.__save_to_file(self.get_entities().values())

    def __load_data(self):
        with open(self.__file_name) as f:
            for line in f:
                if not line.isspace():
                    tokens = line.split(";")
                    client = Client(tokens[0], tokens[1])
                    super().save(client)