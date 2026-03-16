from django.contrib import admin
from .models import Author, Publisher, Book, Genre, Loan

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Loan)
