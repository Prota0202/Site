"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from personal.views import home_screen_view
from account import views

from django.urls import path, include
from personal.views import (
    home_screen_view,
)

from account.views import (
    checkout_view,
    registration_view,
    logout_view,
    login_view,
    account_view,
    forgotPswd_view,
    shop_view,
    add_to_cart,  
    delete_from_cart,    
    cart_view,
    confirm_checkout,    
    order_history_view,  
    users_view,  
    orders_view,
    basket_view,
    delete_all_cart,
    my_orders_view,
    items_view,
    changePromo,
    empty_cart,
)

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', home_screen_view, name='home'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('account/', account_view, name='account'),
    path('forgotPswd/', forgotPswd_view, name='forgotPswd'),
    path('shop/', shop_view, name='shop'),
    path('add-to-cart/<str:product_name>/', add_to_cart, name='add_to_cart'),
    path('changePromo/<str:item_name>/<str:new_data>/', changePromo, name='changePromo'),
    path('delete-from-cart/<str:product_name>/', delete_from_cart, name='delete_from_cart'),
    path('delete-all-cart/', delete_all_cart, name='delete_all_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/confirm/', confirm_checkout, name='confirm_checkout'),
    path('account/orders/', order_history_view, name='order_history'),
    path("mongo/", include("mongo.urls")),
    path('users/', users_view, name='users'),
    path('orders/', orders_view, name='orders'),
    path('basket/', basket_view, name='basket'),
    path('myOrders/', my_orders_view, name='myOrders'),
    path('items/', items_view, name='items'),
    path('empty_cart/', empty_cart, name= 'empty_cart'),

]
