

from domain.validators import LibraryException
from iterable.module_iterable_filter_sort import IterableObject


class RepositoryException(LibraryException):
    pass


class Repository:
    def __init__(self,entities:IterableObject):
        self.__entities= entities

    def find_by_id(self, entity_id):
        """
        Returns the entity if it exists, None otherwise
        :param entity_id:  the id of the entity
        :return: the entity or none
        """
        if entity_id in self.__entities:
            return self.__entities
        return None

    def save(self, entity):
        """
        Saves the entity in the dictionary , the key being the id
        :param entity:
        :return:
        """
        if self.find_by_id(entity.id) is not None:
            raise RepositoryException('This is a duplicate id')

        self.__entities[entity.id] = entity

    def remove(self, entity_id):
        """
        Removes and entity by id
        :param entity:
        :return:
        """
        if self.find_by_id(entity_id) is not None:
            a=self.__entities[entity_id]
            del self.__entities[entity_id]
            return a
        else:
            raise RepositoryException('This id doesnt exist')

    def print_all(self):
        """
        Returns all entities
        :return:
        """
        a = list(self.__entities.values())
        if len(a) > 0:
            return a
        else:
            raise RepositoryException('There are no entities to print')

    def get_entities(self):
        return self.__entities
