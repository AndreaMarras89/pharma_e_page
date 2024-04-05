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

        data_invoicing = response_invoicing.json()

        response_order = requests.post(
            f"{BACKEND_URL}/orders",
            json={"user_ID": DEFAULT_USER_ID},
        )
        data_order = response_order.json()

        response_removal = requests.post(
            f"{BACKEND_URL}/product_removal_all",
            json={"user_id": DEFAULT_USER_ID},
        )
        data_removal = response_removal.json()

        if response_invoicing.status_code == 200:
            order_id = data_order["order_id"]
            removal_bool = data_removal["removed"]
            return render(request, "order_successfull.html")
        else:
            return JsonResponse({"success": False, "error": "Failed"})
    else:
        return JsonResponse({"error": "GET method not allowed"})