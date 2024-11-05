from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm
from account.forms import AccountUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, CartItem
from django.views.decorators.http import require_POST
from .models import Order
from mongo.models import Item, User, Order
from django.core.paginator import Paginator
import random
from django.contrib.auth.forms import AuthenticationForm
from .forms import EmailAuthenticationForm 
from datetime import datetime
from django.views.decorators.cache import cache_page
from django.core.cache import cache


is_connected = False

def order_history_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    orders = Order.objects.filter(user=request.user)
    return render(request, 'account/order_history.html', {'orders': orders})




def confirm_checkout(request):
    date_str = datetime.now().strftime("%d-%m-%Y")
    username= request.session.get('username', False)
    basket = request.session.get('basket', False)
    price = request.session.get('total2', False)
    Order.create_order(date_str, username, basket, price)
    context = {
        'is_connected': request.session.get('is_connected', False),
        'isAdmin' : request.session.get('isAdmin', False),
        'message': 'Merci pour votre achat !'
    }
    return render(request, 'account/confirmation.html', context)


def empty_cart(request):
    request.session['basket']= []
    products = Item.get_items()
    
    is_promotion_filter = request.GET.get('filter') == 'promo'
    price_filter = request.GET.get('filter') == 'prix'

    if is_promotion_filter:
        items = Item.find({'promotion': True})
    else:
        items = Item.get_items()
    

    if price_filter:
        items = sorted(items, key=lambda x: x['price']) 

    paginator = Paginator(items, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    
    context = {
        'page_obj': page_obj,
        'is_promotion_filter': is_promotion_filter, 
        'price_filter': price_filter,
        'products': products,
        'is_connected': request.session.get('is_connected', False),
        'isAdmin' : request.session.get('isAdmin', False)
    }
    

    return render(request, 'account/shop.html', context)

def checkout_view(request):
   
    cart_items = CartItem.objects.all()
    
    
    subtotal = sum(item.total_price() for item in cart_items)
    shipping_cost = 5
    total = sum(shipping_cost for item in cart_items) + subtotal
    context = {
        'is_connected': request.session.get('is_connected', False),
        'isAdmin' : request.session.get('isAdmin', False),
        'basket': request.session.get('basket', False),
        'total': request.session.get('total', False),
        'total2': request.session.get('total2', False),

    }

    
    return render(request, 'account/checkout.html', context)




@require_POST
def delete_from_cart(request, product_name):
   if 'basket' in request.session:
        basket = request.session['basket']

        product_id = Item.get_id(product_name)
        product_to_remove = Item.get_item(product_id)

        if isinstance(basket, list):
            # Recherchez le premier produit correspondant et supprimez-le
            for product in basket:
                # Comparer par l'identifiant du produit
                if product['_id'] == product_to_remove['_id']:
                    basket.remove(product)
                    break  # Arrêtez-vous après avoir supprimé une instance

            # Mettre à jour le panier dans la session
            request.session['basket'] = basket

        basket = request.session.get('basket', False)
        request.session['total']= 0
        request.session['total2']= 0
        for basket in basket:
            request.session['total']+= basket['price']
         

        request.session['total2']=(request.session.get('total', False)+10)

        context = {
            'is_connected': request.session.get('is_connected', False),
            'isAdmin': request.session.get('isAdmin', False),
            'basket': request.session.get('basket', []), 
            'total': request.session.get('total', False),
            'total2': request.session.get('total2', False),
        }
        return render(request, 'account/basket.html', context)

@require_POST
def delete_all_cart(request):
    if 'basket' in request.session:
        basket = request.session['basket']

        request.session['basket'] = []

    context = {
        'is_connected': request.session.get('is_connected', False),
        'isAdmin' : request.session.get('is_connected', False),
        'basket': request.session.get('basket', False),

    }
    return render(request, 'account/basket.html', context)


@require_POST
def add_to_cart(request, product_name):
    print(product_name)
    product_id= Item.get_id(product_name)
    product =Item.get_item(product_id)
    request.session['basket'].append(product)
    request.session.modified = True


    products = Product.objects.all()
    
    
    is_promotion_filter = request.GET.get('filter') == 'promo'
    price_filter = request.GET.get('filter') == 'prix'

    if is_promotion_filter:
        items = Item.find({'promotion': True})
    else:
        items = Item.get_items()
    

    if price_filter:
        items = sorted(items, key=lambda x: x['price']) 
    paginator = Paginator(items, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    context = {
        'page_obj': page_obj,
        'products': products,
        'is_connected': request.session.get('is_connected', False),
        'isAdmin' : request.session.get('isAdmin', False)
    }

    return redirect('shop')

def cart_view(request):
    cart_items = CartItem.objects.all()
    total = sum(item.total_price() for item in cart_items)
    quantity_range = range(1, 11)

    return render(request, 'account/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'quantity_range': quantity_range,
        'is_connected': request.session.get('is_connected', False),
        'isAdmin' : request.session.get('isAdmin', False),
    })


def registration_view(request):
    context = {}
    if request.POST:
        if(request.POST.get('password1') == request.POST.get('password2')):
            email = request.POST.get('email') 
            username = request.POST.get('username')  
            password = request.POST.get('password1')
            User.create_user(username,password,False, email)
            return redirect('login')
       
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    if 'is_connected' in request.session:
        del request.session['is_connected']

    if 'isAdmin' in request.session:
        del request.session['isAdmin']

    return redirect('home')

def forgotPswd_view(request):
    if request.method == 'POST':
        if(request.POST.get('password1') == request.POST.get('password2')):
            email = request.POST.get('email')  
            password = request.POST.get('password1')
            User.update_pswd(email,password)
        return redirect('login')  

    return render(request, 'account/forgotPswd.html')

@cache_page(60 * 15)  # 15 min
def shop_view(request):
    products = Item.get_items()
    
    
    is_promotion_filter = request.GET.get('filter') == 'promo'
    price_filter = request.GET.get('filter') == 'prix'

    cache_key = f"shop_view_{'promo' if is_promotion_filter else 'all'}_{'prix' if price_filter else 'none'}"

    items = cache.get(cache_key)

    if items is None:
        if is_promotion_filter:
            items = Item.find({'promotion': True})
        else:
            items = Item.get_items()

        if price_filter:
            items = sorted(items, key=lambda x: x['price'])

        
        cache.set(cache_key, items, 60 * 15) #15min


    paginator = Paginator(items, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    
    context = {
        'page_obj': page_obj,
        'is_promotion_filter': is_promotion_filter, 
        'price_filter': price_filter,
        'products': products,
        'is_connected': request.session.get('is_connected', False),
        'isAdmin' : request.session.get('isAdmin', False)
    }
    return render(request, 'account/shop.html', context)



def login_view(request):
    request.session['basket']= []
    is_connected = False
    if request.method == 'POST':
        username = request.POST.get('email')  
        password = request.POST.get('password')
        user=User.get_user_by_email(username)
        if(user["password"]== password):
            request.session['is_connected'] = True
            request.session['isAdmin']= False
            isAdmin = request.session['isAdmin']
            request.session['username'] = user["username"]
            request.session['password'] = user["password"]
            request.session['email'] = user['email']
            if(user["isAdmin"] == True):
                request.session['isAdmin'] = True
                isAdmin = request.session['isAdmin']
            return render(request, 'account/home.html', {'is_connected': True, 'isAdmin': isAdmin}) 
        else:
            return render(request, 'account/login.html', {'is_connected': is_connected}) 
    else:
        form = AuthenticationForm()  

    return render(request, 'account/login.html', {'is_connected': is_connected})



def account_view(request):
    is_connected = request.session.get('is_connected', False)
    if not is_connected:
        return redirect('login')


    context = {
        'is_connected': request.session.get('is_connected', False),
        'isAdmin' : request.session.get('isAdmin', False),
        'username': request.session.get('username', False),
        'password': request.session.get('password', False),
        'email': request.session.get('email', False),

    }

    return render(request, 'account/account.html', context)



def users_view(request):
    users = User.get_users()

    filter_type = request.GET.get('filter', '')

    if filter_type == 'isAdmin':
        users = User.find({'isAdmin': True})
        
    elif filter_type == 'isNotAdmin':
        users = User.find({'isAdmin': False})

    search_query = request.GET.get('search', '')

    if search_query:
        users = [user for user in users if search_query.lower() in user['username'].lower()]

    
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'search_query': search_query,
        'filter_admin': filter_type,
        'is_connected': request.session.get('is_connected', False),
        'isAdmin': request.session.get('isAdmin', False),
        'page_obj': page_obj,
    }

    return render(request, 'account/users.html', context)

def orders_view(request):
    orders= Order.get_orders()
    request.session['orders'] = orders

    context = {
        'is_connected': request.session.get('is_connected', False),
        'isAdmin' : request.session.get('isAdmin', False),
        'orders': request.session.get('orders', False),

    }
    return render(request, 'account/orders.html', context)


def basket_view(request):
    basket = request.session.get('basket', False)
    request.session['total']= 0
    request.session['total2']= 0
    for basket in basket:
        request.session['total']+= basket['price']
         

    request.session['total2']=(request.session.get('total', False)+10)
    context = {
        'is_connected': request.session.get('is_connected', False),
        'isAdmin' : request.session.get('isAdmin', False),
        'basket': request.session.get('basket', False),
        'total': request.session.get('total', False),
        'total2': request.session.get('total2', False),

    }
    return render(request, 'account/basket.html', context)



def my_orders_view(request):
    username = request.session.get('username', False)
    orders = Order.get_order(username)
    request.session['orders'] = orders

    context = {
        'is_connected': request.session.get('is_connected', False),
        'isAdmin' : request.session.get('isAdmin', False),
        'orders': request.session.get('orders', False),

    }
    return render(request, 'account/myOrders.html', context)


def items_view(request):
    items = Item.get_items() 


    filter_type = request.GET.get('filter', '')

    if filter_type == 'isPromo':
        items = Item.find({'promotion': True})
    elif filter_type == 'Nopromo':
        items = Item.find({'promotion': False})

    search_query = request.GET.get('search', '')

    if search_query:
        items = [item for item in items if search_query.lower() in item['name'].lower()]

    paginator = Paginator(items, 20)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 
     

    context = {
        'is_connected': request.session.get('is_connected', False),
        'isAdmin': request.session.get('isAdmin', False),
        'search_query': search_query,
        'filter_type': filter_type,
        'items': page_obj,  
        'page_obj': page_obj, 
    }
    return render(request, 'account/items.html', context)



def changePromo(request, item_name,new_data):
    Item.update_item_promo(item_name, new_data)
    items = Item.get_items()  

    
    filter_type = request.GET.get('filter', '')

    if filter_type == 'isPromo':
        items = Item.find({'promotion': True})
    elif filter_type == 'Nopromo':
        items = Item.find({'promotion': False})

    search_query = request.GET.get('search', '')

    if search_query:
        items = [item for item in items if search_query.lower() in item['name'].lower()]

    paginator = Paginator(items, 20)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)  

    context = {
        'is_connected': request.session.get('is_connected', False),
        'isAdmin': request.session.get('isAdmin', False),
        'search_query': search_query,
        'filter_type': filter_type,
        'items': page_obj,  
        'page_obj': page_obj, 
    }
    return render(request, 'account/items.html', context)

