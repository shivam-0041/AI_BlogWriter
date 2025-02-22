from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class NewUsers(models.Model):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=32)
    class Meta:
        db_table="NewUsers"



class BlogPost(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    link=models.URLField()
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


