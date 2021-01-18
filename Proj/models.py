from django.db import models
from taggit.managers import TaggableManager


class User(models.Model):
    my_id = models.CharField(max_length=100, default='admin', primary_key=True)
    pw = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    ph = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    sex = models.IntegerField(default=0)
    region = models.IntegerField(default=0)
    avg_time = models.IntegerField(default=0)
    food_choice = models.IntegerField(default=0)
    age = models.IntegerField(default=20)

    
    def __str__(self):
        return self.my_id

class Board(models.Model):
    boardnum = models.IntegerField(default=0, primary_key=True)
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title


class Text(models.Model):
    boardnumber = models.ForeignKey('Board', null=True, blank=True, on_delete=models.CASCADE)
    text_title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    star = models.IntegerField(default=0)
    tags = TaggableManager(blank=True)
    user = models.CharField(max_length=100, default='default')

    def __str__(self):
        return self.text_title