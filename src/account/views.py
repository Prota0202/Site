from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm
from account.forms import AccountUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, CartItem
from django.views.decorators.http import require_POST
from .models import Order
from mongo.models import Item, User
from django.core.paginator import Paginator
import random
from django.contrib.auth.forms import AuthenticationForm
from .forms import EmailAuthenticationForm 



def order_history_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    orders = Order.objects.filter(user=request.user)
    return render(request, 'account/order_history.html', {'orders': orders})




def confirm_checkout(request):
    return render(request, 'account/confirmation.html', {'message': 'Merci pour votre achat !'})

def checkout_view(request):
   
    cart_items = CartItem.objects.all()
    
    
    subtotal = sum(item.total_price() for item in cart_items)
    shipping_cost = 5
    total = sum(shipping_cost for item in cart_items) + subtotal
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total

    }
    
    return render(request, 'account/checkout.html', context)


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

   
    cart_items = CartItem.objects.all()
    cart_items_data = [
        {"product_name": item.product.name, "quantity": item.quantity, "total_price": item.total_price()}
        for item in cart_items
    ]
    total = sum(item.total_price() for item in cart_items)

   
    return JsonResponse({
        "success": True,
        "cart_items": cart_items_data,
        "total": total
    })

def cart_view(request):
    cart_items = CartItem.objects.all()
    total = sum(item.total_price() for item in cart_items)
    quantity_range = range(1, 11)

    return render(request, 'account/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'quantity_range': quantity_range
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
    return redirect('home')

def forgotPswd_view(request):
    if request.method == 'POST':
        if(request.POST.get('password1') == request.POST.get('password2')):
            email = request.POST.get('email')  
            password = request.POST.get('password1')
            User.update_pswd(email,password)
        return redirect('login')  # ou toute autre page pertinente

    return render(request, 'account/forgotPswd.html')

def shop_view(request):
    products = Product.objects.all()
    
    is_promotion_filter = request.GET.get('filter') == 'promo'
    price_filter = request.GET.get('filter') == 'prix'

    if is_promotion_filter:
        items = Item.find({'promotion': True})
    else:
        items = Item.get_items()
    
    random.shuffle(items)

    if price_filter:
        items = sorted(items, key=lambda x: x['price']) 

    paginator = Paginator(items, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Récupère les éléments pour la page en cours

    context = {
        'page_obj': page_obj,
        'is_promotion_filter': is_promotion_filter, 
        'price_filter': price_filter,
        'products': products,
    }

    return render(request, 'account/shop.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')  
        password = request.POST.get('password')
        user=User.get_user_by_email(username)
        if(user["password"]== password):
            return redirect('home')   
    else:
        form = AuthenticationForm()  

    return render(request, 'account/login.html')



def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST["email"],
                "username": request.POST["username"],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
        form = AccountUpdateForm(
            initial={
                'username': request.user.username,
                'email': request.user.email,
            }
        )

    context['account_form'] = form
    return render(request, 'account/account.html', context)



def users_view(request):
    
    users = User.get_users()

    filter_type = request.GET.get('filter', '')

    if filter_type == 'isAdmin':
        users = User.find({'isAdmin': True})
        print(users)
    elif filter_type == 'isNotAdmin':
        users = User.find({'isAdmin': False})
        print(users)

    search_query = request.GET.get('search', '')

    if search_query:
        users = [user for user in users if search_query.lower() in user['username'].lower()]

    context = {
        'users': users,
        'search_query': search_query,
        'filter_admin': filter_type
    }

    return render(request, 'account/users.html', context)

