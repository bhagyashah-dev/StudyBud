from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from . models import Room, Topic
from .forms import RoomForm

# from django.http import HttpResponse

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'I am a developer'},

# ]

def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password Does not Exist')

    context={'page': page}
    return render(request, 'myapp/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form  = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")

    return render(request, 'myapp/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    context={'rooms':rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'myapp/home.html', context)

def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    context = {'room' : room}
    return render(request, 'myapp/room.html', context)

# def room(request):
#     return HttpResponse('ROOM')

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            topic_name = request.POST.get('topic', '').strip()
            if topic_name:
                topic, created = Topic.objects.get_or_create(name=topic_name)
                room = form.save(commit=False)
                room.host = request.user
                room.topic = topic
                room.save()
                return redirect('home')
            else:
                messages.error(request, 'Topic is required')

    context= {'form':form, 'topics':topics}
    return render(request, 'myapp/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed Here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            topic_name = request.POST.get('topic', '').strip()
            if topic_name:
                topic, created = Topic.objects.get_or_create(name=topic_name)
                room = form.save(commit=False)
                room.topic = topic
                room.save()
                return redirect('home')
            else:
                messages.error(request, 'Topic is required')

    context={'form':form, 'topics':topics, 'room':room}
    return render(request, 'myapp/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'myapp/delete.html', {'obj':room})
