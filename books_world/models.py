from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FavoriteBooks(models.Model):
    guest_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bookId = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('guest_id', 'bookId')

class BookReview(models.Model):
    guest_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=200)
    reviewInput=models.TextField()

class BookSearch(models.Model):
    guest_id = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
