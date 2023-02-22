from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse

import os
from dotenv import load_dotenv
from pathlib import Path
import stripe

from .models import Item

dotenv_path = os.path.join( Path(__file__).resolve().parent.parent , '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

stripe.api_key = os.environ.get("STRIPE_API_KEY")


def index(request):
    return render(request, 'service/index.html' , {'items' : Item.objects.all()})


def getItem(request,id):
    return render(request, 'service/item.html' , {'item' : get_object_or_404(Item, pk=id)})


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


def successPaymernt(request):
    return render(request , 'service/success.html')

def failedPaymernt(request):
    return render(request , 'service/failed.html')