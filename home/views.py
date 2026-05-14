#PROJECT BY INDRASISH BISWAS
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from instamojo_wrapper import Instamojo
from django.conf import settings

# Mock payment gateway for development - comment out if using real Instamojo
MOCK_PAYMENT = True

if not MOCK_PAYMENT:
    api=Instamojo(api_key=settwings.API_KEY,
                auth_token=settings.AUTH_TOKEN,
                endpoint='https://test.instamojo.com/api/1.1/'
                )

# Create your views here.

def home(request):
    pizzas = Pizza.objects.all()
    context = {'pizzas': pizzas}
    return render(request, 'home.html', context)

def login_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user= User.objects.filter(username=username)
            if not user.exists():
                messages.warning(request, "User not found")
                return redirect('/login/')

            user= authenticate(
                username=username,
                password=password
            )
            if user:
                login(request, user)
                return redirect('/')
            messages.error(request, "Wrong password")
            return redirect('/login/')
        
        except Exception as e:
            messages.error(request, "Something went wrong")
            return render(request, 'login.html')
        
    return render(request, 'login.html')

def  register_page(request):
    if request.method == "POST":
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')

            user= User.objects.filter(username=username)
            if user.exists():
                messages.info(request, "Username already taken")
                return redirect('/register/')

            user= User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password
            )

            user.set_password(password)
            user.save()
            messages.success(request, "Account created successfully")
            return redirect('/register/')
        
        except Exception as e:
            messages.error(request, "Something went wrong")
            return render(request, 'register.html')

    # For GET (or any non-POST) requests, show the registration form
    return render(request, 'register.html')

@login_required(login_url='/login/')
def add_cart(request, pizza_uid):
    user = request.user
    pizza_obj = Pizza.objects.get(uid=pizza_uid)    
    cart , _ = Cart.objects.get_or_create(user=user, is_paid=False)

    cart_items = CartItem.objects.create(
            cart=cart,
            pizza=pizza_obj
        )

    return redirect('/')

@login_required(login_url='/login/')
def cart(request):
    cart = Cart.objects.get(user=request.user, is_paid=False)

    payment_url = None
    
    if MOCK_PAYMENT:
        # Mock payment - generates a dummy payment URL for testing
        payment_url = f"http://127.0.0.1:8000/success/?order_id={cart.uid}&amount={cart.get_cart_total()}"
    else:
            response = api.payment_request_create(
                amount = cart.get_cart_total(),
                purpose = "Order",
                buyer_name = request.user.username,
                email = "indrasish.biswas2006@gmail.com",
                redirect_url = "http://127.0.0.1:8000/success/"
            )
            payment_url = response['payment_request']['longurl']
            cart.instamojo_id = response['payment_request']['id']
            cart.save()
        
    context = {'carts': cart, 'payment_url': payment_url}
    
    return render(request, 'cart.html', context)

@login_required(login_url='/login/')
def remove_cart_items(request, cart_item_uid):
    try:
        CartItem.objects.get(uid=cart_item_uid).delete()

        return redirect('/cart/')
    except Exception as e:
        print(e)


@login_required(login_url='/login/')
def orders(request):
    orders = Cart.objects.filter(user=request.user, is_paid=True)
    context = {'orders': orders}
    return render(request, 'orders.html', context)

@login_required(login_url='/login/')
def success(request):
    """Handle successful payment"""
    order_id = request.GET.get('order_id')
    cart = Cart.objects.get(uid=order_id, user=request.user)
    cart.is_paid = True
    cart.save()
    return redirect('/orders/')
        

def logout_page(request):
    logout(request)
    return redirect('/login/')