from django.contrib import admin
from .models import FavoriteBooks, BookReview, BookSearch
# Register your models here.
admin.site.register(FavoriteBooks)
admin.site.register(BookReview)
admin.site.register(BookSearch)