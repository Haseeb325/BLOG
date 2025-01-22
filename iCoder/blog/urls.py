from django.contrib import admin
from django.urls import path

from .views import *
urlpatterns =[

    # Api to post a comment
    path('postComment',postComment  ,name="postComment"),

    path('',blogHome, name="blogHome"),
    path('<str:slug>/', blogPost, name="blogPost")
]