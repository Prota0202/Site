from django.contrib import admin
from account.models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('username', 'email', 'date_joined', 'last_login','is_admin','is_staff')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(Account, AccountAdmin)


