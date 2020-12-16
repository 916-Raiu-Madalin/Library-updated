from datetime import datetime

from domain.entities import Rental


class RentalService:
    def __init__(self, rental_repository, validator, book_repository, client_repository):
        self.__rental_repository = rental_repository
        self.__validator = validator
        self.__book_repository = book_repository
        self.__client_repository = client_repository

    def add_rental(self, rental_id, book_id, client_id, rented_date, returned_date='This book is not returned yet'):
        """
        This method adds a rental
        :param rental_id:
        :param book_id:
        :param client_id:
        :param rented_date:
        :param returned_date:

        """
        p = Rental(rental_id, book_id, client_id, rented_date, returned_date)
        self.__validator.validate_rental(self.__rental_repository, self.__book_repository, self.__client_repository, p)
        self.__rental_repository.save(p)

    def print_rentals(self):
        return self.__rental_repository.print_all()

    def set_return_date(self, rental_id, return_date):
        """
        This method sets the date in which the book was returned
        :param rental_id:
        :param return_date:
        :return:
        """
        a = self.__rental_repository.get_entities()
        self.__validator.validate_return(a[rental_id], return_date)
        if a is None:
            raise Exception('This id doesnt exist')
        elif a[rental_id].data != 'This book is not returned yet':
            raise Exception('This book has been returned already')
        else:
            book_id =a[rental_id].book_id
            client_id=a[rental_id].client_id
            rented_date=a[rental_id].rented_date
            self.remove_rental(rental_id)
            self.add_rental(rental_id,book_id,client_id,rented_date,return_date)

    def most_rented_books(self):
        """
        This method calculates how many times each book has been rented and returns the list of books
        and the numbers for each one in descending order
        :return:
        """
        cop = self.__book_repository.get_entities()
        rental = self.__rental_repository.get_entities()
        book = []
        number = [0] * len(cop)
        for i in rental:
            if cop[rental[i].book_id].title not in book:
                book.append(cop[rental[i].book_id].title)
                number[book.index(cop[rental[i].book_id].title)] = 1
            else:
                number[book.index(cop[rental[i].book_id].title)] += 1
        n = len(number)
        for i in cop:
            if cop[i].title not in book:
                book.append(cop[i].title)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if number[j] < number[j + 1]:
                    number[j], number[j + 1] = number[j + 1], number[j]
                    book[j], book[j + 1] = book[j + 1], book[j]
        return book, number

    def most_rented_authors(self):
        """
        This method calculates how many times each author has been rented and returns the list of authors
        and the numbers for each one in descending order
        :return:
        """
        cop = self.__book_repository.get_entities()
        rental = self.__rental_repository.get_entities()
        authors = []
        number = [0] * len(cop)
        for i in rental:
            if cop[rental[i].book_id].author not in authors:
                authors.append(cop[rental[i].book_id].author)
                number[authors.index(cop[rental[i].book_id].author)] = 1
            else:
                number[authors.index(cop[rental[i].book_id].author)] += 1
        n = len(number)
        for i in cop:
            if cop[i].author not in authors:
                authors.append(cop[i].author)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if number[j] < number[j + 1]:
                    number[j], number[j + 1] = number[j + 1], number[j]
                    authors[j], authors[j + 1] = authors[j + 1], authors[j]
        return authors, number

    def most_active_clients(self):
        """
        This method calculates how many days each client has rented books and returns the list of clients
        and the numbers for each one in descending order
        :return:
        """
        cop = self.__client_repository.get_entities()
        rental = self.__rental_repository.get_entities()
        clients = []
        number = [0] * len(cop)
        for i in cop:
            clients.append(cop[i].name)

        for i in rental:

            if rental[i].data != 'This book is not returned yet\n' and rental[i].data !='This book is not returned yet':
                if len(rental[i].data) > 10:
                    rentals = rental[i].data[:-1]
                else:
                    rentals= rental[i].data
                date_format = '%d/%m/%Y'
                a = datetime.strptime(rental[i].rented_date, date_format)
                b = datetime.strptime(rentals, date_format)
                aux = b - a
                number[clients.index(cop[rental[i].client_id].name)] += aux.days

        n = len(number)

        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if number[j] < number[j + 1]:
                    number[j], number[j + 1] = number[j + 1], number[j]
                    clients[j], clients[j + 1] = clients[j + 1], clients[j]
        return clients, number

    def get_entities(self):
        return self.__rental_repository.get_entities()

    def remove_rental(self, rental_id):
        """
        This method removes the rental from the given id

        """
        self.__rental_repository.remove(rental_id)
