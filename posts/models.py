from django.db import models

# Create your models here.
"""
class Post:
    id int
    title sting
    content text
    created datetime 
    updated datetime
"""
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    createdAt= models.DateTimeField(auto_now_add= True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

