from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages

import os
from dotenv import load_dotenv
from pathlib import Path
import stripe

from django.contrib.auth.models import User
from .models import Item, Order

dotenv_path = os.path.join( Path(__file__).resolve().parent.parent , '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

stripe.api_key = os.environ.get("STRIPE_API_KEY")


def index(request):
    return render(request, 'service/index.html' , {'items' : Item.objects.all()})


def getItem(request,id):
    return render(request, 'service/item.html' , {'item' : get_object_or_404(Item, pk=id)})

def successPaymernt(request):
    return render(request , 'service/success.html')

def failedPaymernt(request):
    return render(request , 'service/failed.html')

def create_checkout_session(request , id):

    item = Item.objects.get(id=id)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': item.currency.lower(),
                'product_data': {
                    'name': item.name,
                },
                'unit_amount_decimal': item.price * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:4242/failed',
    )
    return JsonResponse({"url" : session.url})


def register(request):

    if request.method == 'POST' : 
        username = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(username = username).exists() :
            messages.info(request, 'Username already used.')
            return redirect('register')
        else : 
            user = User.objects.create_user(username=username,password=password)
            user.save()
            messages.success(request, 'Register was successfully.')
            return redirect('login')

    return render(request , 'service/register.html')

def addItemToOrder(request,id):

    if request.user.is_authenticated:
        item = Item.objects.get(pk=id)
        Order.objects.create(user = request.user, item = item)
        return redirect(f'http://127.0.0.1:8000/item/{id}')
    else :
        return redirect('login')


def getOrder(request):

    return render(request , 'service/order.html' , {'items' : Order.objects.filter(user = request.user)})

def clearOrder(request):
    Order.objects.filter(user = request.user).delete()
    return redirect('home')

def paymentOrder(request) : 

    line_items = []
    for line in list(Order.objects.filter(user = request.user)):
 
        line_items.append({
            'price_data': {
                'currency': line.item.currency.lower(),
                'product_data': {
                    'name': line.item.name,
                },
                'unit_amount_decimal': line.item.price * 100,
            },
            'quantity': 1,
        })
    
    session = stripe.checkout.Session.create(
        line_items= line_items,
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/failed',
    )
    return JsonResponse({"url" : session.url})
