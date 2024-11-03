from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate , logout
from account.forms import RegistrationForm, AccountAuthenticationForm
from account.forms import AccountUpdateForm
from mongo.models import Item, User
from django.core.paginator import Paginator
import random

# Create your views here.

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')


from django.shortcuts import render

def forgotPswd_view(request):
    # Si c'est une requête POST, traitez le formulaire ici
    if request.method == 'POST':
        # Logique pour traiter la demande de réinitialisation de mot de passe
        # ...

        # Rediriger vers une autre page après traitement, par exemple la page de confirmation
        return redirect('login')  # ou toute autre page pertinente

    # Si c'est une requête GET, afficher le formulaire de réinitialisation
    return render(request, 'account/forgotPswd.html')  # Assurez-vous d'avoir ce template


def shop_view(request):
    
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
        'price_filter': price_filter 
    }

    return render(request, 'account/shop.html', context)


def login_view(request):
    context = {}
    
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
        
    context['login_form'] = form
    return render(request, 'account/login.html', context)

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
