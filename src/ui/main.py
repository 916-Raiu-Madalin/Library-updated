
import traceback


from Repositories.binary_file_repo import  BinaryFileRepository
from Repositories.books_file_repo import BooksFileRepository
from Repositories.clients_file_repo import ClientsFileRepository
from Repositories.rentals_file_repo import RentalsFileRepository
from Repositories.repository import Repository
from domain.validators import BookValidator, ClientValidator, RentalValidator
from services.BookService import BookService
from services.ClientService import ClientService
from services.RentalService import RentalService
from settings.settings import Settings

from ui.console import Console

if __name__ == '__main__':
    settings = Settings("../settings.properties")
    config = settings.get_the_settings()
    try:
        if config[0] == "inmemory":
            book_validator = BookValidator()
            client_validator = ClientValidator()
            rental_validator = RentalValidator()

            book_repository = Repository({})
            client_repository = Repository({})
            rental_repository = Repository({})

            book_service = BookService(book_repository, book_validator)
            client_service = ClientService(client_repository, client_validator)
            rental_service = RentalService(rental_repository, rental_validator, book_repository, client_repository)

            console = Console(book_service, client_service, rental_service)
            console.run_console()
        elif config[0] == "filerepository":
            book_validator = BookValidator()
            client_validator = ClientValidator()
            rental_validator = RentalValidator()

            book_repository = BooksFileRepository(config[1])
            client_repository = ClientsFileRepository(config[2])
            rental_repository = RentalsFileRepository(config[3])

            book_service = BookService(book_repository, book_validator)
            client_service = ClientService(client_repository, client_validator)
            rental_service = RentalService(rental_repository, rental_validator, book_repository, client_repository)

            console = Console(book_service, client_service, rental_service)
            console.run_console()
        elif config[0] == "binaryfiles":
            book_validator = BookValidator()
            client_validator = ClientValidator()
            rental_validator = RentalValidator()

            book_repository = BinaryFileRepository(config[1])
            client_repository = BinaryFileRepository(config[2])
            rental_repository = BinaryFileRepository(config[3])

            book_service = BookService(book_repository, book_validator)
            client_service = ClientService(client_repository, client_validator)
            rental_service = RentalService(rental_repository, rental_validator, book_repository, client_repository)

            console = Console(book_service, client_service, rental_service)
            console.run_console()
    except Exception as ex:
        print('Unexpected exception! ', ex)
        traceback.print_exc()
