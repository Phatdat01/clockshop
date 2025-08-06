from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import json

# Create your views here.
def home(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = 'hidden'
        user_login = 'visible'
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        user_not_login = 'visible'
        user_login = 'hidden'
        cartItems = order['get_cart_items']
    context = {'products': products, 'cartItems': cartItems, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'app/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added to cart', safe=False)

def temp_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return HttpResponse('User registered successfully')
    return render(request, 'app/register.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'app/register.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is not incorrect')
    context = {}
    return render(request, 'app/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('login')

def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        keys = Product.objects.filter(name__contains=search_query)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    return render(request, 'app/search.html', {"search":search_query,'keys': keys, 'cartItems': cartItems, 'products': products})