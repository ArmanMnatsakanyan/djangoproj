from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} of {self.author}'
