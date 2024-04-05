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

def error(request):
    return render(request, "error_page.html")

def emptyCartWarning(request):
    return render(request, "empty_cart_warning.html")

def catalogue(request):
    response = requests.get(f"{BACKEND_URL}/products_list")
    if response.status_code == 200:
        data = response.json()
        return render(
            request,
            "catalogue.html",
            {
                "products": data["products"],
            },
        )
    return redirect("/webapp/error_page.html")
    
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
            return redirect("/webapp/error_page.html")
    else:
        return redirect("/webapp/error_page.html")
    
def productDetails(request):
    return render(request, "details.html")
    
def showCart(request):
    response = requests.post(
        f"{BACKEND_URL}/cart_details",
        json={"user_id": DEFAULT_USER_ID},
    )
    if response.status_code == 200:
        data = response.json()
        return render(
            request,
            "cart.html",
            {
                "products": data["products"],
            },
        )
    return redirect("/webapp/error_page.html")


def showBuy(request):
    response = requests.post(
        f"{BACKEND_URL}/cart_details",
        json={"user_id": DEFAULT_USER_ID},
    )
    if response.status_code == 200:
        data = response.json()
        if len(data["products"]) == 0:
            return redirect("/webapp/empty_cart_warning.html")
        return render(request, "buy.html")        
    else:
        return redirect("/webapp/error_page.html")


def goToDetails(request, product_id):
    response = requests.post(
        f"{BACKEND_URL}/product_details", json={"product_id": product_id}
    )
    if response.status_code == 200:
        data = response.json()
        return render(
            request,
            "details.html",
            {
                "product_name": data["product_name"],
                "product_description": data["product_description"],
                "product_price": data["product_price"],
                "availability": True if data["quantity"] > 0 else False,
                "image": data["product_image"]
            },
        )
    return redirect("/webapp/error_page.html")


def InvoiceInformation(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        cf = request.POST.get("cf")
        address = request.POST.get("address")
        billing_address = request.POST.get("billing_address")
        response_invoicing = requests.post(
           f"{BACKEND_URL}/info_invoicing",
            json={
                "user_ID": DEFAULT_USER_ID,
                "name": first_name,
                "last_name": last_name,
                "cf": cf,
                "address": address,
                "billing_address": billing_address,
            },
        )
        if response_invoicing.status_code != 200:
            return redirect("/webapp/error_page.html")

        data_invoicing = response_invoicing.json()
        
        response_order = requests.post(
            f"{BACKEND_URL}/orders",
            json={"user_ID": DEFAULT_USER_ID},
        )
        
        if response_order.status_code != 200:
            return redirect("/webapp/error_page.html")
        
        data_order = response_order.json()
        
        response_removal = requests.post(
            f"{BACKEND_URL}/product_removal_all",
            json={"user_id": DEFAULT_USER_ID},
        )
        
        if response_removal.status_code != 200:
            return redirect("/webapp/error_page.html")
        
        data_removal = response_removal.json()

        order_id = data_order["order_id"]
        removal_bool = data_removal["removed"]
        return render(request, "order_successfull.html")
    

def orderHistory(request):
    response = requests.post(f"{BACKEND_URL}/order_history", json={"user_id": DEFAULT_USER_ID})
    if response.status_code == 200:
        data = response.json()
        return render(
            request,
            "order_history.html",
            {
                "orders": data["orders_list"]
            }
        )
    return redirect("/webapp/error_page.html")


def emptyTheCart(request):
    response_removal = requests.post(
            f"{BACKEND_URL}/product_removal_all",
            json={"user_id": DEFAULT_USER_ID},
        )
        
    if response_removal.status_code != 200:
        return redirect("/webapp/error_page.html")
    
    data_removal = response_removal.json()
    return redirect("/webapp/cart.html")