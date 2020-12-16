from enum import Enum

from services.RedoService import RedoService
from services.UndoService import UndoService


# -------------------------undo book------------------------------------
def undo_add_book(book_service, book_id):
    """
    undo add book operation

    """
    a = book_service.get_entities()
    title = a[book_id].title
    author = a[book_id].author
    a=book_service.remove_book(book_id)
    RedoService.store_operation(book_service, RedoHandler.REDO_ADD_BOOK, book_id, title, author)



def undo_remove_book(book_service, book_id, title, author):
    """
   undo remove book
    """
    book_service.add_book(book_id, title, author)
    RedoService.store_operation(book_service, RedoHandler.REDO_REMOVE_BOOK, book_id)


def undo_update_book(book_service, book_id, title, author):
    """
    undo  update book
    """
    a = book_service.get_entities()
    old_title = a[book_id].title
    old_author = a[book_id].author
    book_service.remove_book(book_id)
    book_service.add_book(book_id, title, author)
    RedoService.store_operation(book_service, RedoHandler.REDO_UPDATE_BOOK, book_id, old_title, old_author)


# --------------------------undo client------------------------------------
def undo_add_client(client_service, client_id):
    """
    undo add client operation

    """
    a = client_service.get_entities()
    name = a[client_id].name
    client_service.remove_client(client_id)
    RedoService.store_operation(client_service, RedoHandler.REDO_ADD_CLIENT, client_id, name)


def undo_remove_client(client_service, client_id, name):
    """
   undo remove book
    """
    client_service.add_client(client_id, name)
    RedoService.store_operation(client_service, RedoHandler.REDO_REMOVE_CLIENT, client_id)


def undo_update_client(client_service, client_id, name):
    """
    undo  update client
    """
    a = client_service.get_entities()
    old_name = a[client_id].name
    client_service.remove_client(client_id)
    client_service.add_client(client_id, name)
    RedoService.store_operation(client_service, RedoHandler.REDO_UPDATE_CLIENT, client_id, old_name)


# -----------------------undo rental---------------
def undo_add_rental(rental_service, rental_id):
    a = rental_service.get_entities()
    book_id = a[rental_id].book_id
    client_id = a[rental_id].client_id
    rented_date = a[rental_id].rented_date
    returned_date = a[rental_id].data

    rental_service.remove_rental(rental_id)
    RedoService.store_operation(rental_service, RedoHandler.REDO_ADD_RENTAL, rental_id, book_id, client_id, rented_date,
                                returned_date)


class UndoHandler(Enum):
    UNDO_ADD_BOOK = undo_add_book
    UNDO_REMOVE_BOOK = undo_remove_book
    UNDO_UPDATE_BOOK = undo_update_book

    UNDO_ADD_CLIENT = undo_add_client
    UNDO_REMOVE_CLIENT = undo_remove_client
    UNDO_UPDATE_CLIENT = undo_update_client

    UNDO_ADD_RENTAL = undo_add_rental


# --------------------------redo book------------------------------------

def redo_add_book(book_service, book_id, title, author):
    book_service.add_book(book_id, title, author)
    UndoService.store_operation(book_service, UndoHandler.UNDO_ADD_BOOK, book_id)


def redo_remove_book(book_service, book_id):
    a = book_service.get_entities()
    title = a[book_id].title
    author = a[book_id].author
    book_service.remove_book(book_id)
    UndoService.store_operation(book_service, UndoHandler.UNDO_REMOVE_BOOK, book_id, title, author)

def redo_update_book(book_service, book_id, title, author):
    """
    Handles redo update book operation
    """
    a = book_service.get_entities()
    old_title = a[book_id].title
    old_author = a[book_id].author
    book_service.remove_book(book_id)
    book_service.add_book(book_id, title, author)
    UndoService.store_operation(book_service, UndoHandler.UNDO_UPDATE_BOOK, book_id, old_title, old_author)


# --------------------------redo client------------------------------------

def redo_add_client(client_service, client_id, name):
    client_service.add_client(client_id, name)
    UndoService.store_operation(client_service, UndoHandler.UNDO_ADD_CLIENT, client_id)


def redo_remove_client(client_service, client_id):
    a = client_service.get_entities()
    name = a[client_id].name
    client_service.remove_client(client_id)
    UndoService.store_operation(client_service, UndoHandler.UNDO_REMOVE_CLIENT, client_id, name)


def redo_update_client(client_service, client_id, name):
    """
    Handles redo update client operation
    """
    a = client_service.get_entities()
    old_name = a[client_id].name
    client_service.remove_client(client_id)
    client_service.add_client(client_id, name)
    UndoService.store_operation(client_service, UndoHandler.UNDO_UPDATE_CLIENT, client_id, old_name)


def redo_add_rental(rental_service, rental_id, book_id, client_id, rented_date, return_date):
    rental_service.add_rental(rental_id,book_id,client_id,rented_date,return_date)
    UndoService.store_operation(rental_service, UndoHandler.UNDO_ADD_RENTAL, rental_id)


class RedoHandler(Enum):
    REDO_ADD_BOOK = redo_add_book
    REDO_REMOVE_BOOK = redo_remove_book
    REDO_UPDATE_BOOK = redo_update_book

    REDO_ADD_CLIENT = redo_add_client
    REDO_REMOVE_CLIENT = redo_remove_client
    REDO_UPDATE_CLIENT = redo_update_client

    REDO_ADD_RENTAL = redo_add_rental
