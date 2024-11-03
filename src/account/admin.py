from django.contrib import admin
from .models import Account, Product, CartItem, Order, OrderItem
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')

    # Enlevez les champs qui n'existent pas dans votre modèle personnalisé
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser', 'is_active')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Supprimez les champs non définis de filter_horizontal et list_filter
    filter_horizontal = ()
    list_filter = ('is_admin', 'is_staff', 'is_active')

admin.site.register(Account, AccountAdmin)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)

