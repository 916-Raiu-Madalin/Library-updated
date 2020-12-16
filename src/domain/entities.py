# this is where the books and client classes are defined

class Book:
    def __init__(self, book_id, title, author):
        self.__book_id = book_id
        self.__title = title
        self.__author = author

    @property
    def id(self):
        return self.__book_id

    @id.setter
    def id(self, value):
        self.__book_id = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        self.__author = value

    def __str__(self) -> str:
        return "{0} {1}   {2}".format(self.__book_id, self.__title, self.__author)


class Client:
    def __init__(self, client_id, name):
        self.__client_id = client_id
        self.__name = name

    @property
    def id(self):
        return self.__client_id

    @id.setter
    def id(self, value):
        self.__client_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def __str__(self) -> str:
        return "{0} {1}".format(self.__client_id, self.__name)


class Rental:
    def __init__(self, rental_id, book_id, client_id, rented_date, return_date):
        self.__rental_id = rental_id
        self.__book_id = book_id
        self.__client_id = client_id
        self.__rented_date = rented_date
        self.__return_date = return_date

    @property
    def id(self):
        return self.__rental_id

    @property
    def book_id(self):
        return self.__book_id

    @property
    def client_id(self):
        return self.__client_id

    @property
    def rented_date(self):
        return self.__rented_date

    @property
    def data(self):
        return self.__return_date

    def data_(self, value):
        self.__return_date = value

    def __str__(self) -> str:
        return "{0} {1} {2} {3} {4}".format(self.__rental_id, self.__book_id, self.__client_id, self.__rented_date,
                                            self.__return_date)
