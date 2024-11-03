from django.shortcuts import render
from account.models import Account
# Create your views here.

def home_screen_view(request):
    
    context = {}
    accounts = Account.objects.all()
    context = {
        'accounts' : accounts,
         'is_connected': request.session.get('is_connected', False),
         'isAdmin' : request.session.get('isAdmin', False)
    }

    
    return render(request, "personal/home.html", context)