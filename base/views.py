from turtle import end_fill
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from urllib3 import encode_multipart_formdata
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {"id": 1, "name": "Learn python"},
#     {"id": 2, "name": "Django Developers"},
#     {"id": 3, "name": "ML Engineers"}
# ]

# queryResult = ModelObj.objects.get(attribut='value')


def home(req):
    # return HttpResponse("Home page")
 
    q = req.GET.get('q') if req.GET.get('q') != None else ''
    # rooms = Room.objects.filter(topic__name__icontains=q, name__icontains=q) #this requires q to match all parameters
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count=rooms.count()
    context = {"rooms": rooms, "topics": topics, "room_count":room_count}
    return render(req, 'base/home.html', context)


def room(req, pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    # room = {"name": "learn withme broxk", "id": 2}
    context = {"room": room}
    return render(req, 'base/room.html', context)

def createRoom(req):
    form = RoomForm()
    if req.method == 'POST':
        form = RoomForm(req.POST)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(req, 'base/room_form.html', context)

def updateRoom(req, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)
    if req.method == 'POST':
        form = RoomForm(req.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(req, 'base/room_form.html', context)
    
def deleteRoom(req, pk):
    room = Room.objects.get(id=pk)
    if req.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj':"\'"+room.name+"\' room"}
    return render(req, 'base/delete.html', context)

def loginView(req):
    context={}
    return render(req, 'base/login_register.html', context)