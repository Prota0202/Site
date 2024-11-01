from django.urls import path
from . import views

urlpatterns = [
    path('user/create/', views.create_user, name='create_user'),
    path('user/create-multiple/', views.create_multiple_users, name='create_multiple_users'),
    path('user/<str:user_id>/', views.get_user, name='get_user'),
    path('users/', views.get_users, name='get_users'),
    path('user/<str:user_id>/update/', views.update_user, name='update_user'),
    path('user/<str:user_id>/delete/', views.delete_user, name='delete_user'),
    path('item/create/', views.create_item, name='create_item'),
    path('item/create-multiple/', views.create_multiple_items, name='create_multiple_items'),
    path('item/<str:item_id>/', views.get_item, name='get_item'),
    path('items/', views.get_items, name='get_items'),
    path('item/<str:item_id>/update/', views.update_item, name='update_item'),
    path('item/<str:item_id>/delete/', views.delete_item, name='delete_item'),
]
