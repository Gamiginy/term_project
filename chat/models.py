from django.db import models
from auction.models import Book


# Create your models here.
class Chat(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    message = models.TextField()
