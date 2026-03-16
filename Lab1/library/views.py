from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Book, Author, Loan

def author_list(request):
    authors = Author.objects.all()
    return render(request, "library/author_list.html", {"authors": authors})

def author_info(request, author_id):
    author = Author.objects.get(id=author_id)
    books = Book.objects.filter(authors=author)
    context = {
        "author": author,
        "books": books,
    }
    return render(request, "library/author_info.html", context)

def home(request):
    context = {
        "authors_count": Author.objects.count(),
        "books_count": Book.objects.count(),
        "users_count": User.objects.count(),
    }
    return render(request, "library/home.html", context)

def book_list(request):
    books = Book.objects.all()
    return render(request, "library/book_list.html", {"books": books})

def book_info(request, book_id):
    book = Book.objects.get(id=book_id)
    active_loan = None
    if request.user.is_authenticated:
        active_loan = Loan.objects.filter(
            user=request.user,
            book=book,
            returned_at__isnull=True,
        ).first()
    return render(request, "library/book_info.html", {"book": book, "active_loan": active_loan})

@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)
    active_loan = Loan.objects.filter(
        user=request.user,
        book=book,
        returned_at__isnull=True,
    ).first()
    if request.method == "POST" and active_loan is None and book.available_count > 0:
        Loan.objects.create(user=request.user, book=book)
    return redirect("book_info", book_id=book.id)

@login_required
def return_book(request, book_id):
    book = Book.objects.get(id=book_id)
    active_loan = Loan.objects.filter(
        user=request.user,
        book=book,
        returned_at__isnull=True,
    ).first()
    if request.method == "POST" and active_loan:
        active_loan.returned_at = timezone.now()
        active_loan.save()
    return redirect("book_info", book_id=book.id)
