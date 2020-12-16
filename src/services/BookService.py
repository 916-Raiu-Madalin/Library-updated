from domain.entities import Book
from iterable.module_iterable_filter_sort import filter_entities, shell_sort


class BookService:
    def __init__(self, book_repository, validator):
        self.__book_repository = book_repository
        self.__validator = validator

    def add_book(self, book_id, title, author):
        """
        This method adds a book
        :param book_id:
        :param title:
        :param author:
        :return:
        """
        p = Book(book_id, title, author)
        self.__validator.validate_book(p)
        self.__book_repository.save(p)

    def remove_book(self, book_id):
        """
        This method removes the book from the given id
        :param book_id:
        :return:
        """
        self.__book_repository.remove(book_id)

    def print_books(self):
        return self.__book_repository.print_all()

    def search_book_by_id(self, value):
        """
        This method finds the books that have a similar id and returns the books
        :param value:the id we search by
        :return: The list of books with similar id
        """

        # cop = self.__book_repository.get_entities()
        # plist = []
        # for i in cop:
        #     if value in cop[i].id:
        #         plist.append(cop[i])
        # plist = filter_entities(cop, search_criteria())

        def sort_criteria_author(entity1, entity2):
            return entity1.id < entity2.id

        def search_criteria_id(key):
            return value in key.id

        cop =self.get_entities()
        entities= list(cop.values())

        plist = filter_entities(entities, search_criteria_id)
        shell_sort(plist, sort_criteria_author)
        return plist

    def search_book_by_author(self, author):
        """
        This method finds the authors that have similar name with the given one
        :param author: the name
        :return: the list of books with the given or similar author
        """

        # cop = self.__book_repository.get_entities()
        # plist = []
        # for i in cop:
        #     if author.lower() in cop[i].author.lower():
        #         plist.append(cop[i])

        def sort_criteria_author(name1, name2):
            return name1.author < name2.author

        def search_criteria_author(key):
            return author.lower() in key.author.lower()

        cop = self.get_entities()
        entities = list(cop.values())

        plist = filter_entities(entities, search_criteria_author)
        shell_sort(plist, sort_criteria_author)

        return plist

    def search_book_by_title(self, title):
        """
        This method finds the books with the given title
        :param title:
        :return: the list of books with this title or titles that have a similarity with the parameter
        """

        # cop = self.__book_repository.get_entities()
        # plist = []
        # for i in cop:
        #     if title.lower() in cop[i].title.lower():
        #         plist.append(cop[i])

        def sort_criteria_title(name1, name2):
            return name1.title < name2.title

        def search_criteria_title(key):
            return title.lower() in key.title.lower()

        cop = self.get_entities()
        entities = list(cop.values())

        plist = filter_entities(entities, search_criteria_title)
        shell_sort(plist, sort_criteria_title)

        return plist

    def get_entities(self):
        return self.__book_repository.get_entities()
