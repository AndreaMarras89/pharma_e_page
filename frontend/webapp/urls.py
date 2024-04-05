from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path("home.html", views.home, name="home"),
    path("", views.home, name="home"),
    path("catalogue.html", views.catalogue, name="catalogue"),
]