from django.contrib import admin
from django.urls import path

from .views import *
urlpatterns =[
    path('',home, name="home"),
    path('contact/',contact, name="contact"),
    path('about/',about, name="about"),
    path('search', search, name="search"),
    path('signup', handleSignup, name="handleSignup"),
    path('login', handleLogin, name="handleLogin"),
    path('logout', handleLogout, name="handleLogout"),
]