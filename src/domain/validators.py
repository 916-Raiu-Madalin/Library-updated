class LibraryException(Exception):
    pass


class BookValidatorException(LibraryException):
    pass


class ClientValidatorException(LibraryException):
    pass


class RentalValidatorException(LibraryException):
    pass


class BookValidator:
    @staticmethod
    def validate_book(book):
        if not book.id.isdigit():
            raise BookValidatorException('The id has to be a positive number')
        if book.author.isdigit():
            raise BookValidatorException('The name cant contain a digit')


class ClientValidator:
    @staticmethod
    def validate_client(client):

        if client.name.isdigit():
            raise ClientValidatorException('The name cant contain a digit')


class RentalValidator:
    @staticmethod
    def validate_rental(rents, book, client, rental):
        a = rental.rented_date.split('/')

        if not a[0].isdigit() or not a[1].isdigit() or not a[2].isdigit():
            raise RentalValidatorException('The date needs to be formed of digits')
        a = rents.get_entities()
        b = book.get_entities()
        c = client.get_entities()
        for i in a:
            if a[i] == rental.id:
                raise RentalValidatorException('This rental id exists already')
            if a[i].data == 'This book is not returned yet\n' and a[i].book_id == rental.book_id:
                raise RentalValidatorException('This book cant be rented')
        if rental.book_id not in b:
            raise RentalValidatorException('This book doesnt exist')
        if rental.client_id not in c:
            raise RentalValidatorException('This client doesnt exist')

    @staticmethod
    def validate_return(rental, return_d):
        a = rental.rented_date.split('/')
        b = return_d.split('/')
        if rental.data != 'This book is not returned yet\n' and rental.data !='This book is not returned yet':
            raise RentalValidatorException('This book has been returned already')
        if int(a[2]) > int(b[2]):
            raise RentalValidatorException('You cant return the book before you rent it buddy')
        elif int(a[2]) == int(b[2]):
            if int(a[1]) > int(b[1]):
                raise RentalValidatorException('You cant return the book before you rent it buddy')
            elif int(a[1]) == int(b[1]):
                if int(a[0]) > int(b[0]):
                    raise RentalValidatorException('You cant return the book before you rent it buddy')
