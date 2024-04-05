import requests
from django import template
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from frontend.settings import BACKEND_URL, DEFAULT_USER_ID


register = template.Library


def home(request):
    return render(request, "home.html")


def catalogue(request):
    response = requests.get(f"{BACKEND_URL}/products_list")
    data = response.json()
    return render(
        request,
        "catalogue.html",
        {
            "products": data["products"],
        },
    )
    
def addToCart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        response = requests.post(
            f"{BACKEND_URL}/add_product",
            json={
                "user_id": DEFAULT_USER_ID,
                "product_id": product_id,
                "quantity": 1,
            },
        )
        if response.status_code == 200:
            return redirect("/webapp/catalogue.html")
        else:
            return JsonResponse(
                {"success": False, "error": "Failed to add product to cart"}
            )
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})
    
def showCart(request):
    response = requests.post(
        f"{BACKEND_URL}/cart_details",
        json={"user_id": DEFAULT_USER_ID},
    )
    data = response.json()
    return render(
        request,
        "cart.html",
        {
            "products": data["products"],
        },
    )


def showBuy(request):
    return render(request, "buy.html")