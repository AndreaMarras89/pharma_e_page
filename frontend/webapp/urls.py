from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path("home.html", views.home, name="home"),
    path("", views.home, name="home"),
    path("catalogue.html", views.catalogue, name="catalogue"),
    path("addToCart/", views.addToCart, name="addToCart"),
    path("cart.html", views.showCart, name="showCart"),
    path("buy.html", views.showBuy, name="buy"),
]