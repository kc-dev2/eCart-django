from django.db import models
from django.core.validators import RegexValidator
from django.db.models import Sum
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

# Create your models here.
class Customer(models.Model):
    """
    Contains email, username, and references Cart model
    """
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Username can only contain alphanumeric characters.')

    email_id = models.EmailField(unique=True)
    username = models.CharField(max_length=50, validators = [alphanumeric])
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email_id


class Cart(models.Model):
    """
    Contains id and total costs of Product models
    """
    cart_id = models.SmallAutoField(primary_key=True)
    customer = models.OneToOneField(
        'Customer',
        on_delete=models.CASCADE,
        related_name = 'my_cart',
        null = True
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return "Cart {}, {}".format(str(self.cart_id),str(self.customer))


class Vendor(models.Model):
    """
    Contains vendor id, name, Product models sold by vendor, and quantity of each Product model
    """
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Username can only contain alphanumeric characters.')

    vendor_email = models.EmailField(unique = True, null = True)
    vendor_name = models.CharField(max_length=50, validators = [alphanumeric])

    def __str__(self):
        return str(self.vendor_email)


class Product(models.Model):
    """
    Contains product id, name, creation date, and cart that it is a part of
    """
    name_regex = RegexValidator('^[0-9a-zA-Z]+([0-9a-zA-Z ]+)*$', 'Product name can only contain alphanumeric characters and cannot start/end with whitespace.')

    # alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Username can only contain alphanumeric characters.')

    prod_id = models.SmallAutoField(primary_key=True)
    prod_name = models.CharField(max_length=100, validators = [name_regex])
    sold_by = models.ManyToManyField('Vendor', related_name = 'products', blank = True)
    total_quantity = models.SmallIntegerField(default=1)
    added_on = models.DateField(auto_now_add=True)


    def __str__(self):
        return str(self.prod_name)


class VendorProduct(models.Model):
    """
    Contains product id, vendor_id of selling vendor, and quantity
    """
    prod_id = models.ForeignKey('Product', on_delete=models.CASCADE, null = True)
    vendor_id = models.ForeignKey('Vendor', on_delete = models.CASCADE, related_name = 'products_to_sell', null = True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity_left = models.SmallIntegerField(default=1)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['prod_id', 'vendor_id'], name='unique_prod_vendor_pair')]

    def __str__(self):
        return "{1} (vendor: {0})".format(str(self.vendor_id.vendor_name), str(self.prod_id))



class CartProduct(models.Model):
    """
    Contains product id, cart_id of purchasing cart, and quantity in cart
    """
    cart = models.ForeignKey('Cart', on_delete = models.CASCADE, related_name = 'products_in_cart', blank = True)
    product = models.ForeignKey('VendorProduct', on_delete = models.CASCADE)
    # could maybe add cost as another field
    quantity_wanted = models.SmallIntegerField(default=1)

    def __str__(self):
        return "{}, {}".format(str(self.cart), str(self.product))

    class Meta:
        constraints = [models.UniqueConstraint(fields=['product', 'cart'], name='unique_prod_cart_pair')]


""" Method to run apart from instance creations (post_save, etc.)"""
def create_cart_for_customer(sender, instance, **kwargs):
    # Get the cart that matches the incoming customer instance
    try:
        ref_cart = Cart.objects.get(customer_id__id = instance.id)
    except:
        # If not cart can be found given the customer instance, that means we are creating a new
        # Customer instance so we have to also create a new Cart instance for that Customer
        new_cart = Cart()
        new_cart.save()
        new_cart.customer_id = instance   # honestly, idk why it's 'customer_id'
        new_cart.save()


def set_prod_quantity(sender, instance, **kwargs):
    if instance.prod_id is not None:
        ref_prod = instance.prod_id
        sum_quantity = VendorProduct.objects.filter(prod_id = ref_prod).aggregate(Sum('quantity_left'))['quantity_left__sum']

        prod = Product.objects.get(prod_id = ref_prod.prod_id)
        prod.total_quantity = sum_quantity
        prod.save()

def check_prod_quantity(sender, instance, **kwargs):
    # save or delete Product object based on total quantity left
    prod_to_check = Product.objects.get(prod_id = instance.prod_id_id)
    prod_to_check.total_quantity -= instance.prod_id.total_quantity
    if prod_to_check.total_quantity == 0:
        prod_to_check.delete()
    else:
        prod_to_check.save()

def venDel_SET_prod_quantity(sender, instance, **kwargs):
    for ven_prod in instance.products_to_sell.all():
        prod = Product.objects.get(prod_id = ven_prod.prod_id.prod_id)
        prod.total_quantity -= ven_prod.quantity_left
        prod.save()
        if prod.total_quantity == 0:
            prod.delete()

def cart_modified(sender, instance, **kwargs):
    if instance.cart_id is not None:
        update_sum = 0
        curr_cart = Cart.objects.get(cart_id = instance.cart_id)
        # sum up costs of all cart products in current cart
        for prod in curr_cart.products_in_cart.all():
            update_sum += prod.quantity_wanted * prod.product.unit_cost

        curr_cart.total = update_sum
        curr_cart.save()

""" Methods to connect to post/pre save/delete methods above """
# After saving Customer instance, check if new Cart has to be created
post_save.connect(create_cart_for_customer, sender = Customer)
post_save.connect(set_prod_quantity, sender = VendorProduct)
post_delete.connect(check_prod_quantity, sender = VendorProduct)
pre_delete.connect(venDel_SET_prod_quantity, sender = Vendor)
post_save.connect(cart_modified, sender=CartProduct)
post_delete.connect(cart_modified, sender=CartProduct)
