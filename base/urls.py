from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),  # pk -> primary key
    path("create-room/", views.createRoom, name='createRoom'), 
    path("update-room/<str:pk>/", views.updateRoom, name='updateRoom'),
    path("delete-room/<str:pk>/", views.deleteRoom, name='deleteRoom'),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerView, name="register"),
    path("delete-msg/<str:pk>/", views.deleteMessage, name="deleteMsg"),
    path("profile/<str:pk>", views.userProfile, name="user-profile")
]
