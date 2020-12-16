from Repositories.repository import Repository, RepositoryException
from domain.entities import Book, Client
from domain.validators import BookValidator, ClientValidator, RentalValidator, RentalValidatorException, \
    ClientValidatorException, BookValidatorException
from iterable.module_iterable_filter_sort import IterableObject, shell_sort
from services.BookService import BookService
from services.ClientService import ClientService
from services.RedoService import RedoService, RedoException
from services.RentalService import RentalService
import unittest

from services.UndoRedoService import UndoHandler, RedoHandler
from services.UndoService import UndoService, UndoException


class TestEntity(unittest.TestCase):
    a = Book('1', "Test", "me")
    a.id = '2'
    a.title = "TEst1"
    a.author = "MESS"
    b = Client('1', "Test")
    b.id = "2"
    b.name = "me"


class TestRepo(unittest.TestCase):
    def setUp(self):
        self._repo = Repository({})
        self._repo.save(Book('1', "The Dream", 'Jack Sparrow'))
        self._repo.save(Book('2', "Good Day", 'Salam de Sibiu'))
        self._repo.save(Book('3', "I have no Ideea", 'Someone'))
        self._repo.save(Book('4', "The legend", 'Guta'))
        self._repo.save(Book('5', "Unknown", 'Nicoae Balcescu'))
        self._repo.save(Book('6', "Cocalar", 'Dani Mocanu'))
        try:
            self._repo.save(Book('6', "Cocalar", 'Dani Mocanu'))
        except RepositoryException:
            pass

    def test_repo_save(self):
        a = self._repo.get_entities()
        self.assertNotEqual(len(a), 0)
        self.assertIn('1', a)
        self.assertIn('2', a)
        self.assertIn('3', a)
        self.assertIn('4', a)
        self.assertIn('5', a)
        self.assertIn('6', a)
        self.assertIs('Jack Sparrow', a['1'].author)
        self.assertEqual(len(a), 6)

    def test_find_by(self):
        self.assertEqual(self._repo.find_by_id('12'), None)
        self.assertNotEqual(self._repo.find_by_id('1'), None)

    def test_remove(self):
        self._repo.remove('1')
        self.assertEqual(self._repo.find_by_id('1'), None)
        try:
            self._repo.remove('1')
        except RepositoryException:
            pass


class TestBookService(unittest.TestCase):
    def setUp(self):
        self._book_validator = BookValidator()
        self._book_repository = Repository({})
        self._book_service = BookService(self._book_repository, self._book_validator)
        self._book_service.add_book('1', 'The Book', 'King Arthur')
        self._book_service.add_book('2', 'The Prize', 'Im Somebody')
        self._book_service.add_book('3', 'Im Out Of Ideeas', 'Some random dude')
        try:
            self._book_service.add_book('4', '4', '434')
        except BookValidatorException:
            pass

    def test_book_add(self):
        a = self._book_repository.get_entities()
        self.assertEqual(len(a), 3)
        self.assertEqual(a['1'].title, 'The Book')
        self.assertEqual(a['1'].author, 'King Arthur')
        self.assertEqual(a['2'].title, 'The Prize')
        self.assertEqual(a['2'].author, 'Im Somebody')

    def test_book_remove(self):
        self._book_service.remove_book('1')
        a = self._book_repository.get_entities()
        self.assertEqual(len(a), 2)
        self.assertEqual(self._book_repository.find_by_id('1'), None)

    def test_search_by_id(self):
        a = self._book_service.search_book_by_id('1')
        self.assertEqual(a[0].id, '1')
        self.assertEqual(a[0].author, 'King Arthur')
        self.assertEqual(a[0].title, 'The Book')

    def test_search_by_title(self):
        a = self._book_service.search_book_by_title('The')
        self.assertEqual(a[0].id, '1')
        self.assertEqual(a[0].author, 'King Arthur')
        self.assertEqual(a[0].title, 'The Book')
        self.assertEqual(len(a), 2)
        self.assertEqual(a[1].id, '2')
        self.assertEqual(a[1].author, 'Im Somebody')
        self.assertEqual(a[1].title, 'The Prize')

    def test_search_by_author(self):
        a = self._book_service.search_book_by_author('King')
        self.assertEqual(a[0].id, '1')
        self.assertEqual(a[0].author, 'King Arthur')
        self.assertEqual(a[0].title, 'The Book')


class TestClientService(unittest.TestCase):
    def setUp(self):
        self._client_validator = ClientValidator()
        self._client_repository = Repository({})
        self._client_service = ClientService(self._client_repository, self._client_validator)
        self._client_service.add_client('1', 'King Arthur')
        self._client_service.add_client('2', 'Im Somebody')
        self._client_service.add_client('3', 'Some random dude')
        try:
            self._client_service.add_client('4', '43')
        except ClientValidatorException:
            pass

    def test_client_add(self):
        a = self._client_repository.get_entities()

        self.assertEqual(len(a), 3)
        self.assertEqual(a['1'].name, 'King Arthur')
        self.assertEqual(a['2'].name, 'Im Somebody')
        self.assertEqual(a['3'].name, 'Some random dude')

    def test_client_remove(self):
        self._client_service.remove_client('1')
        a = self._client_repository.get_entities()
        assert len(a) == 2
        self.assertEqual(self._client_repository.find_by_id('1'), None)

    def test_search_by_id(self):
        a = self._client_service.search_client_by_id('1')
        self.assertEqual(a[0].id, '1')
        self.assertEqual(a[0].name, 'King Arthur')

    def test_search_by_name(self):
        a = self._client_service.search_client_by_name('King')
        self.assertEqual(a[0].id, '1')
        self.assertEqual(a[0].name, 'King Arthur')
        self.assertEqual(len(a), 1)


class TestRentalService(unittest.TestCase):
    def setUp(self):
        self._book_validator = BookValidator()
        self._book_repository = Repository({})
        self._book_service = BookService(self._book_repository, self._book_validator)
        self._client_validator = ClientValidator()
        self._client_repository = Repository({})
        self._client_service = ClientService(self._client_repository, self._client_validator)
        self._rental_validator = RentalValidator()
        self._rental_repository = Repository({})
        self._rental_service = RentalService(self._rental_repository, self._rental_validator, self._book_repository,self._client_repository)

        self._book_service.add_book('1', 'The Book', 'King Arthur')
        self._book_service.add_book('2', 'The Prize', 'Im Somebody')
        self._book_service.add_book('3', 'Im Out Of Ideeas', 'Some random dude')

        self._client_service.add_client('1', 'Raiu Madalin')
        self._client_service.add_client('2', 'Ristei Elena')
        self._client_service.add_client('3', 'Another random dude')

        self._rental_service.add_rental('1', '2', '3', '10/10/2019')
        self._rental_service.add_rental('2', '1', '2', '02/03/2019')
        try:
            self._rental_service.add_rental('2', '1', '2', '02/03/2019')
        except RentalValidatorException as ve:
            pass
        except RepositoryException:
            pass
        self._rental_service.set_return_date('2', '02/03/2020')
        self._rental_service.add_rental('3', '1', '3', '02/03/2019')
        try:
            self._rental_service.add_rental('4', '3', '1223', '02/03/2019')
        except RentalValidatorException:
            pass
        try:
            self._rental_service.add_rental('134', '444', '1223', '02/03/2019')

        except RentalValidatorException:
            pass
        try:
            self._rental_service.add_rental('134', '3', '2', '02/03/2019')
            self._rental_service.add_rental('134', '3', '2', '02/03/2019')
        except RentalValidatorException:
            pass
        except RepositoryException:
            pass

        try:
            self._rental_service.add_rental('134', '3', '2', '0d/s3/2019')

        except RentalValidatorException:
            pass

    def test_rental_add(self):
        a = self._rental_repository.get_entities()
        self.assertEqual(len(a), 4)
        self.assertEqual(a['1'].book_id, '2')
        self.assertEqual(a['1'].client_id, '3')
        self.assertEqual(a['1'].rented_date, '10/10/2019')
        self.assertEqual(a['1'].data, 'This book is not returned yet')

    def test_rental_return(self):
        a = self._rental_repository.get_entities()
        self.assertEqual(a['1'].data, 'This book is not returned yet')

        self._rental_service.set_return_date('1', '20/10/2020')
        self.assertEqual(a['1'].data, '20/10/2020')
        self.assertEqual(a['3'].data, 'This book is not returned yet')
        try:
            self._rental_service.set_return_date('1', '20/10/2020')
        except RentalValidatorException:
            pass
        try:
            self._rental_service.set_return_date('3', '01/03/2019')
        except RentalValidatorException:
            pass
        try:
            self._rental_service.set_return_date('3', '02/02/2019')

        except RentalValidatorException:
            pass
        try:
            self._rental_service.set_return_date('3', '02/03/2018')

        except RentalValidatorException:
            pass

    def test_most_rented_books(self):
        self._rental_service.set_return_date('1', '20/10/2020')
        a, b = self._rental_service.most_rented_books()
        self.assertEqual(a[0], 'The Book')
        self.assertEqual(b[0], 2)

    def test_most_rented_authors(self):
        a, b = self._rental_service.most_rented_authors()
        self.assertEqual(a[0], 'King Arthur')
        self.assertEqual(b[0], 2)
        self.assertEqual(a[1], 'Im Somebody')
        self.assertEqual(b[1], 1)

    def test_most_active_clients(self):
        self._rental_service.set_return_date('1', '20/10/2020')
        a, b = self._rental_service.most_active_clients()
        self.assertEqual(a[0], 'Another random dude')
        self.assertEqual(b[0], 376)

    def test_rental_print(self):
        a = self._rental_service.print_rentals()
        self.assertNotEqual(len(a), 0)


class TestUndoService(unittest.TestCase):
    def setUp(self):
        """
        Prepare tests
        """
        self.rental_repository = Repository({})
        self.validator2 = RentalValidator()
        self.book_repository = Repository({})
        self.validator = BookValidator()
        self.client_repository = Repository({})
        self.validatorc = ClientValidator()
        self.undo_service = UndoService()
        self.redo_service = RedoService()
        self.book_service = BookService(self.book_repository, self.validator)
        self.client_service = ClientService(self.client_repository, self.validatorc)
        self.rental_service = RentalService(self.rental_repository, self.validator2, self.book_repository,
                                            self.client_repository)

    def test_undo_controller(self):
        """
        Tests for undo controller
        """
        self.assertRaises(UndoException, self.undo_service.do_undo)
        self.assertRaises(RedoException, self.redo_service.do_redo)

        self.book_service.add_book('12', "the name", 'By me')
        self.undo_service.store_operation(self.book_service, UndoHandler.UNDO_ADD_BOOK, '12')
        self.undo_service.do_undo()
        self.assertTrue(len(self.book_service.get_entities()) == 0)
        self.redo_service.store_operation(self.book_service, RedoHandler.REDO_ADD_BOOK, '12', "the name", "By me")

        self.redo_service.do_redo()
        self.assertTrue(len(self.book_service.get_entities()) == 1)
        self.book_service.add_book('2', "the name", 'By me')
        self.book_service.remove_book('2')
        self.undo_service.store_operation(self.book_service, UndoHandler.UNDO_REMOVE_BOOK, '2', "The Mandalorian", "Didu")
        self.undo_service.do_undo()

        self.undo_service.store_operation(self.book_service, UndoHandler.UNDO_UPDATE_BOOK, '2', "The Mandalorian","Didu")
        self.undo_service.do_undo()
        self.redo_service.store_operation(self.book_service, RedoHandler.REDO_UPDATE_BOOK, '2', "The Mandalorian","Didu")
        self.redo_service.do_redo()

        self.client_service.add_client("10", "andrei")
        self.undo_service.store_operation(self.client_service, UndoHandler.UNDO_ADD_CLIENT, '10')
        self.undo_service.do_undo()
        self.assertTrue(len(self.client_service.get_entities()) == 0)
        self.redo_service.store_operation(self.client_service, RedoHandler.REDO_ADD_CLIENT, "10", "andrei")
        self.redo_service.do_redo()
        self.assertTrue(len(self.client_service.get_entities()) == 1)

        self.client_service.remove_client('10')
        self.undo_service.store_operation(self.client_service, UndoHandler.UNDO_REMOVE_CLIENT, '10', 'andrei')
        self.undo_service.do_undo()
        self.redo_service.store_operation(self.client_service, RedoHandler.REDO_REMOVE_CLIENT, '10')
        self.redo_service.do_redo()

        self.client_service.add_client('2', "Didu")
        self.undo_service.store_operation(self.client_service, UndoHandler.UNDO_UPDATE_CLIENT, '2', "Didu")
        self.undo_service.do_undo()
        self.redo_service.store_operation(self.client_service, RedoHandler.REDO_UPDATE_CLIENT, '2', 'Didu')
        self.redo_service.do_redo()

        self.rental_service.add_rental('1', '2', '2', '20/10/2020')
        self.undo_service.store_operation(self.rental_service, UndoHandler.UNDO_ADD_RENTAL, '1')
        self.undo_service.do_undo()
        self.redo_service.store_operation(self.rental_service, RedoHandler.REDO_ADD_RENTAL, '1', '2', '2', '20/10/2020','')
        self.redo_service.do_redo()

        self.book_service.add_book('20', "book", 'By me')
        self.book_service.remove_book('20')
        self.undo_service.store_operation(self.book_service, UndoHandler.UNDO_REMOVE_BOOK, '20', "book", "By me")
        self.undo_service.do_undo()
        self.redo_service.store_operation(self.book_service, RedoHandler.REDO_REMOVE_BOOK, '20')
        self.redo_service.do_redo()

        self.redo_service.clear()


class IterableTests(unittest.TestCase):
    def setUp(self)->None:
        self.__iter = IterableObject()
        self.__iter['1'] = Book("1", "The book", 'Me')
        self.__iter['2'] = Book('2', 'Some name', 'nada')

    def test_iter(self):
        a = self.__iter['1']
        a = len(self.__iter)

        del self.__iter['1']
        self.__iter['1'] = Book("1", "The book", 'Me')
        for obj in self.__iter:
            for ibj in self.__iter:
                ok=1
    @staticmethod
    def sort_key(a, b):
        return a < b

    def test_sort(self):
        listp=[23,54,123,34]
        shell_sort(listp, self.sort_key)

