from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    about = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Publisher(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    publication_date = models.DateField()
    count = models.IntegerField()

    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, blank=True)
    genre = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return self.title

    @property
    def active_loans_count(self):
        return self.loan_set.filter(returned_at__isnull=True).count()

    @property
    def available_count(self):
        return self.count - self.active_loans_count


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(blank=True, null=True)

    def clean(self):
         if self.book.available_count < 0:
             raise ValidationError('No available copies of this book to loan.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)