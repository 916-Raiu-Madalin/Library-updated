import _pickle
import pickle

from Repositories.repository import Repository


class BinaryFileRepository(Repository):
    def __init__(self, file_name):
        super().__init__({})
        self.__file_name = file_name
        self.__load_data()

    def save(self,entity):
        super().save(entity)
        self.save_binary_file(self.get_entities())

    def save_binary_file(self,entity):
        with open(self.__file_name,'wb') as f:
            pickle.dump(entity,f)
            
    def remove(self,entity_id):
        super().remove(entity_id)
        self.save_binary_file(self.get_entities())

    def __load_data(self):
        with open(self.__file_name,"rb") as f:
            try:
                a=pickle.load(f)
                for entity in a:
                    super().save(a[entity])
            except EOFError:
                pass
            except _pickle.UnpicklingError:
                pass