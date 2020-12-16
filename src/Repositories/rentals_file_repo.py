from domain.entities import Rental
from src.Repositories.repository import Repository


class RentalsFileRepository(Repository):
    def __init__(self, file_name):
        super().__init__({})
        self.__file_name = file_name
        self.__load_data()

    def save(self, rental):
        super().save(rental)
        self.__save_to_file(self.get_entities().values())

    def __save_to_file(self, rentals):
        with open(self.__file_name, "w") as f:
            try:
                for rental in rentals:
                    rental_str = str(rental.id) + ';' + str(
                        rental.book_id) + ';' + str(rental.client_id) + ';' + str(rental.rented_date) + ";" + str(
                        rental.data)
                    f.write(rental_str + "\n")

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
                    rental = Rental(tokens[0], tokens[1], tokens[2], tokens[3],tokens[4])
                    super().save(rental)