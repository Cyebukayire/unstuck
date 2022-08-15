from dataclasses import field, fields
from django.forms import ModelForm
from .models import Room
from .models import Message

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        # fields = ['name', 'topic', 'description']
        exclude = ['host', 'participants']
