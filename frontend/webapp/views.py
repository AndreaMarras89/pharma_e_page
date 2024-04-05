import requests
from django import template
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse


register = template.Library


def home(request):
    return render(request, "home.html")


def catalogue(request):
    response = requests.get("http://localhost:8089/products_list")
    data = response.json()
    return render(
        request,
        "catalogue.html",
        {
            "products": data["products"],
        },
    )