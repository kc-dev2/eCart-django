from django.contrib import admin

# Register your models here.
from .models import Customer, Cart, Product, Vendor, VendorProduct, CartProduct

admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(Vendor)
admin.site.register(VendorProduct)
admin.site.register(CartProduct)
