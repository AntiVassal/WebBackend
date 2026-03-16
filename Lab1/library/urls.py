from django.urls import path
from .views import book_list, book_info, author_list, author_info, borrow_book, return_book

urlpatterns = [
    path('books/', book_list),
    path('books/<int:book_id>/', book_info, name="book_info"),
    path('books/<int:book_id>/borrow/', borrow_book, name="borrow_book"),
    path('books/<int:book_id>/return/', return_book, name="return_book"),
    path('authors/', author_list),
    path('authors/<int:author_id>/', author_info, name="author_info"),
]