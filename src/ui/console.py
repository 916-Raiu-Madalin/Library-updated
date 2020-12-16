import random
import traceback

from domain.validators import LibraryException
from services.RedoService import RedoService, RedoException
from services.UndoRedoService import UndoHandler
from services.UndoService import UndoService, UndoException


class Console:
    def __init__(self, book_service, client_service, rental_service):
        self.__book_service = book_service
        self.__client_service = client_service
        self.__rental_service = rental_service
        self.__commands = {1: self.ui_add_book, 2: self.ui_add_client, 3: self.ui_remove_book,
                           4: self.ui_remove_client, 5: self.ui_list_books, 6: self.ui_list_clients,
                           7: self.ui_update_book, 8: self.ui_update_client, 9: self.ui_add_rental,
                           10: self.ui_return, 11: self.ui_print_rentals, 12: self.ui_search_book,
                           13: self.ui_search_client, 14: self.ui_most_rented_books, 15: self.ui_most_rented_authors,
                           16: self.ui_most_active_clients,17:self.ui_undo,18:self.ui_redo}

        # self.random_inputs()
        # self.rent_inputs()

    def rent_inputs(self):
        self.__rental_service.add_rental('1', '1', '1', '10/10/2019')
        self.__rental_service.add_rental('2', '2', '2', '10/9/2018')
        self.__rental_service.add_rental('3', '3', '3', '9/9/2014')

        self.__rental_service.set_return_date('1', '10/10/2020')
        self.__rental_service.set_return_date('3', '10/10/2020')

    def run_console(self):
        self.print_menu()
        while True:
            try:

                cmd = int(input("Choose a number: "))
                if cmd == 19:
                    print('Bye')
                    return
                if cmd in self.__commands:
                    try:
                        self.__commands[cmd]()
                        print('\n')
                    except LibraryException as le:
                        print(le)
                else:
                    print("This option is not yet implemented")
            except ValueError as ve:
                print('Input must be an integer ', ve)
            except Exception as ex:
                print("Unexpected exception" ,ex)
                traceback.print_exc()

    def print_menu(self):
        print("\n1.Add Book        2.Add Client \n"
              "3.Remove book     4.Remove Client \n"
              "5.List Books      6.List Clients \n"
              "7.Update Book     8.Update Client \n"
              "9.Rent a book     10.Return a book \n"
              "11.List Rentals   12.Search Book \n"
              "13.Search Client  14.Rented Books \n"
              "15.Rented Authors 16.Active Clients \n"
              "17.Undo           18.Redo \n"
              "19.Exit \n"

              )

    def ui_add_book(self):
        book_id = input("Book id: ")
        title = input("Title: ")
        author = input("Author: ")
        self.__book_service.add_book(book_id, title, author)
        RedoService.clear()
        UndoService.store_operation(self.__book_service, UndoHandler.UNDO_ADD_BOOK, book_id)

    def ui_add_client(self):
        client_id = input("client id: ")
        name = input("Name: ")
        self.__client_service.add_client(client_id, name)
        RedoService.clear()
        UndoService.store_operation(self.__client_service, UndoHandler.UNDO_ADD_CLIENT, client_id)

    def ui_add_rental(self):
        rental_id = input("Rental id: ")
        book_id = input("Book id: ")
        client_id = input("Client id: ")
        rented_date = input("Rented date in dd/mm/yyyy format: ")
        self.__rental_service.add_rental(rental_id, book_id, client_id, rented_date)
        RedoService.clear()
        UndoService.store_operation(self.__rental_service,UndoHandler.UNDO_ADD_RENTAL,rental_id)

    def ui_remove_book(self):
        book_id = input('Book id: ')
        try:
            a = self.__book_service.get_entities()
            title= a[book_id].title
            author=a[book_id].author
            self.__book_service.remove_book(book_id)
            RedoService.clear()
            UndoService.store_operation(self.__book_service, UndoHandler.UNDO_REMOVE_BOOK, book_id,title,author)
        except KeyError:
            print("There is no book with this id")
    def ui_remove_client(self):
        client_id = input('Client id: ')
        try:
            a =self.__client_service.get_entities()
            name= a[client_id].name
            self.__client_service.remove_client(client_id)
            RedoService.clear()
            UndoService.store_operation(self.__client_service, UndoHandler.UNDO_REMOVE_CLIENT, client_id,name)
        except KeyError:
            print("There is no client with this id")
    def ui_list_books(self):
        a = self.__book_service.print_books()
        print("id  Title         Author")
        for i in a:
            print(i)

    def ui_list_clients(self):
        a = self.__client_service.print_clients()
        print("id   Name")
        for i in a:
            print(i)

    def ui_update_book(self):
        book_id = input("Book id: ")
        title = input("New Title: ")
        author = input("New Author: ")
        try:
            a= self.__book_service.get_entities()
            old_title= a[book_id].title
            old_author= a[book_id].author
            self.__book_service.remove_book(book_id)
            self.__book_service.add_book(book_id, title, author)
            RedoService.clear()
            UndoService.store_operation(self.__book_service,UndoHandler.UNDO_UPDATE_BOOK,book_id,old_title,old_author)
        except KeyError:
            print("There is no such id")
    def ui_update_client(self):
        client_id = input("client id: ")
        name = input("New Name: ")
        try:
            a = self.__client_service.get_entities()
            old_name = a[client_id].name
            self.__client_service.remove_client(client_id)
            self.__client_service.add_client(client_id, name)
            RedoService.clear()
            UndoService.store_operation(self.__client_service, UndoHandler.UNDO_UPDATE_CLIENT, client_id, old_name)
        except KeyError:
            print("There is no such id")
    def ui_print_rentals(self):
        a = self.__rental_service.print_rentals()
        for i in a:
            print(i)

    def ui_return(self):
        rental_id = input("Give rental id: ")
        returned_date = input("Introduce date in dd/mm/yyyy format: ")
        self.__rental_service.set_return_date(rental_id, returned_date)


    def random_inputs(self):
        for i in range(0, 10):
            try:
                self.random_book_title()
                self.random_name()
                self.__book_service.add_book(str(i + 1), self.__title, self.__name)

                self.random_name()
                self.__client_service.add_client(str(i + 1), self.__name)
            except Exception:
                print('')

    def random_book_title(self):
        """
        This is a function that returns a random book title
        :return: a random book title as a string
        """
        names1 = ['Clock', 'Blood', 'Mirror', 'Corpse', 'Painting', 'The', 'Sign', 'Wooden', 'Tuba', 'Trap']
        names2 = ['Kiss', 'Titan', 'Dying', 'Hustle', 'Queen', 'Solaris', 'Avenging', 'Runaway', 'Affair', 'Attack']
        self.__title = ""
        self.__title += random.choice(names1)
        self.__title += ' '
        self.__title += random.choice(names2)

    def random_name(self):
        """
        This is a function that returns a random author name
        :return: a random author name as a string
        """
        name1 = ['Misti', 'Raiu', 'Popescu', 'Risteiu', 'Buda', 'Trump', 'Bocsa', 'Bucea', 'Todea', 'Salam']
        name2 = ['Andrei', 'Augustin', 'Andreea', 'Mihai', 'Mircea', 'Nadia', 'Vali', 'Cristi', 'Daniela', 'Fabian']
        self.__name = ""
        self.__name += random.choice(name1)
        self.__name += ' '
        self.__name += random.choice(name2)

    def random_date(self):
        """
        This function returns a random dd/mm/yyyy date
        :return:
        """
        self.__random_date = ""
        self.__random_date += str(random.randint(1, 28))
        self.__random_date += '/'
        self.__random_date += str(random.randint(1, 12))
        self.__random_date += '/'
        self.__random_date += str(random.randint(2000, 2019))

    def ui_search_book(self):
        print('Which one do you want to search by? \n'
              '1.id   2.Title   3.Author \n')
        cop = []
        try:
            cmd = int(input("Choose a number: "))
            if cmd == 1:
                aux = input('Give id: ')
                cop = self.__book_service.search_book_by_id(aux)
            elif cmd == 2:
                aux = input('Give title: ')
                cop = self.__book_service.search_book_by_title(aux)
            elif cmd == 3:
                aux = input('Give author: ')
                cop = self.__book_service.search_book_by_author(aux)
            else:
                print("This option is not yet implemented")
        except ValueError as ve:
            print('Input must be an integer ', ve)
        if len(cop) == 0:
            print('There is nothing that matches your search criteria!')
        else:
            for i in cop:
                print(i)

    def ui_search_client(self):
        print('Which one do you want to search by? \n'
              '1.id   2.Name  \n')
        cop = []
        try:
            cmd = int(input("Choose a number: "))
            if cmd == 1:
                aux = input('Give id: ')
                cop = self.__client_service.search_client_by_id(aux)
            elif cmd == 2:
                aux = input('Give title: ')
                cop = self.__client_service.search_client_by_name(aux)
            else:
                print("This option is not yet implemented")
        except ValueError as ve:
            print('Input must be an integer ', ve)
        if len(cop) == 0:
            print('There is nothing that matches your search criteria!')
        else:
            for i in cop:
                print(i)

    def ui_most_rented_books(self):
        book, number = self.__rental_service.most_rented_books()
        print("Most rented books:")
        for i in range(len(book)):
            print(str(book[i]) + ' ' + str(number[i]))

    def ui_most_rented_authors(self):
        print("Most rented authors:")
        author, number = self.__rental_service.most_rented_authors()
        for i in range(len(author)):
            print(str(author[i]) + ' ' + str(number[i]))

    def ui_most_active_clients(self):
        print("Most active clients:")
        clients, number = self.__rental_service.most_active_clients()
        for i in range(len(clients)):
            print(str(clients[i]) + ' ' + str(number[i]))

    def ui_undo(self):
        try:
            UndoService.do_undo()
            print("Undo executed")
        except UndoException as ue:
            print(ue)
    def ui_redo(self):
        try:
            RedoService.do_redo()
            print("Redo executed")
        except RedoException as ue:
            print(ue)