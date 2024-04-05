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
    path("order_successfull.html", views.InvoiceInformation, name="InvoiceInformation"),
    path(
        r"goToDetails/(?P<str:product_id>[^/]+)/\\Z/",
        views.goToDetails,
        name="goToDetails",
    ),
    path("details.html", views.productDetails, name="details"),
    path("order_history.html", views.orderHistory, name="order history"),
    path("error_page.html", views.error, name="error"),
    path("emptyTheCart/", views.emptyTheCart, name="emptyTheCart"),
    path("empty_cart_warning.html", views.emptyCartWarning, name="warning_empty_cart")
]