from turtle import end_fill
from django.shortcuts import render
from django.http import HttpResponse
from urllib3 import encode_multipart_formdata

rooms = [
    {"id": 1, "name": "Learn python"},
    {"id": 2, "name": "Django Developers"},
    {"id": 3, "name": "ML Engineers"}
]


def home(req):
    # return HttpResponse("Home page")
    context = {"rooms": rooms}
    return render(req, 'base/home.html', context)


def room(req, pk):
    room = None
    
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {"room": room}
    return render(req, 'base/room.html', context)
