from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.forms import UserCreationForm

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
    # room_messages = Message.objects.all()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )

    context = {"rooms": rooms, "topics": topics, 
    "room_count":room_count, "all_messages": room_messages}
    return render(req, 'base/home.html', context)


def room(req, pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('created') #set works for one to may relationship
    participants = room.participants.all() #this works for many to many relationships
    # room = {"name": "learn withme broxk", "id": 2}

    if req.method=='POST':
        message = Message.objects.create(
            user = req.user,
            room=room,
            body=req.POST.get('body')
        )
        room.participants.add(req.user)
        return redirect('room', pk=pk)

    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(req, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(req):
    form = RoomForm()
    if req.method == 'POST':
        form = RoomForm(req.POST)
        if form.is_valid:
            room = form.save(commit=False)
            room.host = req.user
            room.save()
            return redirect('home')

    context = {'form': form}
    return render(req, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(req, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    if req.user != room.host: #also add to check for Super user
        return HttpResponse("You're not allowed here")
    if req.method == 'POST':
        form = RoomForm(req.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(req, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(req, pk):
    room = Room.objects.get(id=pk)

    if req.user != room.host: #also add to check for Super user
        return HttpResponse("You're not allowed here")

    if req.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj':"\'"+room.name+"\' room"}
    return render(req, 'base/delete.html', context)

def loginView(req):
    page = 'login'
    if req.user.is_authenticated:
        return redirect('home')

    if req.method == 'POST':
        username = req.POST.get('username').lower()
        password=req.POST.get('password')
        
        # check user existance
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(req, 'Username or password is incorrect')

        user = authenticate(req, username=username, password=password)

        # login the user
        if user is not None:
            login(req, user) #this creates session
            return redirect('home')
        else:
            messages.error(req, 'Username or password is incorrect')

    context={'page': page}
    return render(req, 'base/login_register.html', context)

def logoutUser(req):
    logout(req)
    return redirect('login')

def registerView(req):
    form = UserCreationForm()
    
    if req.method=="POST":
        form = UserCreationForm(req.POST)
        try:
            if form.is_valid:
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(req, user) 
                return redirect('home')
            else:
                messages.error(req, 'An error occured during registration')
        except:
            messages.error(req, "An error occured during registration")
    context={"form": form}
    return render(req, 'base/login_register.html', context)

# Messages
def deleteMessage(req, pk):
    message = Message.objects.get(id=pk)

    if req.user != message.user: #also add to check for Super user
        return HttpResponse("You're not allowed here")

    if req.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj': "the message"}
    return render(req, 'base/delete.html', context)


def userProfile(req, pk):
    user = User.objects.get(id=pk)
    rooms= user.room_set.all()
    user_messages=user.message_set.all()
    topics = Topic.objects.all()
    context={"user": user, "rooms": rooms, "all_messages": user_messages, "topics": topics}
    return render(req, 'base/profile.html', context)