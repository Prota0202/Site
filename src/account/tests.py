from django.test import TestCase
from account.models import Order, Account, Product, OrderItem


user = Account.objects.first()  
product = Product.objects.first()  


order = Order.objects.create(user=user)


order_item = OrderItem.objects.create(order=order, product=product, quantity=1)

print(order)
print(order_item)

