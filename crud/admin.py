"""Module to register models to admin platform"""

from django.contrib import admin

# Register your models here.
from .models import BookList

admin.site.register(BookList)
