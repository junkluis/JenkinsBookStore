"""DB/Django Model definitions"""
from django.db import models

# Create your models here.


class BookList(models.Model):
    """BookList model represents a Book instance in DB"""
    title = models.CharField(max_length=150)
    price = models.IntegerField()
    author = models.CharField(max_length=100)

    def __str__(self):
        """unicode representation of model instance 'BookList'"""
        return self.title
