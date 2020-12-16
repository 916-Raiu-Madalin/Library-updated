from domain.entities import Book
from src.Repositories.repository import Repository



class BooksFileRepository(Repository):
    def __init__(self, file_name):
        super().__init__({})
        self.__file_name = file_name
        self.__load_data()

    def save(self, book):
        super().save(book)
        self.__save_to_file(self.get_entities().values())

    def __save_to_file(self, books):
        with open(self.__file_name, "w") as f:
            try:
                for book in books:
                    book_str = str(book.id) + ';' + str(book.title) + ';' + str(book.author)
                    f.write(book_str + "\n")
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
                    book = Book(tokens[0], tokens[1], tokens[2])
                    super().save(book)