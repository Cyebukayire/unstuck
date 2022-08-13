from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)   
    decription=models.TextField(null=True, blank=True) #null for db & blank for form
    # participants=
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        # ordering = ['updated', 'created'] #arranges in ascending
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE) # on delete of the user, this user won't be deleted from the db
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # on_delete for many-to-one relationship  and CASCADE to delete all msgs
    body = models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body

