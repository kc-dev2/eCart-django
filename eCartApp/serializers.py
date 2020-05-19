from rest_framework import serializers

from eCartApp.models import Cart, Customer, Product, Vendor, VendorProduct, CartProduct

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email_id', 'username']

class CartSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    products_in_cart = serializers.StringRelatedField(many=True)
    class Meta:
        model = Cart
        fields = ['customer', 'products_in_cart', 'total']
        read_only_fields = ['customer', 'products_in_cart', 'total']
        # DRF default has depth=0, which refers to depths of relationships that should be
        # traversed before reverting to flat representation. For flat representation, an
        # object is denoted using it's primary key.

class VendorSerializer(serializers.ModelSerializer):
    products_to_sell = serializers.StringRelatedField(many=True)
    class Meta:
        model = Vendor
        fields = ['vendor_email', 'vendor_name', 'products_to_sell']
        read_only_fields = ['products_to_sell']
        depth=1

class ProductSerializer(serializers.ModelSerializer):
    sold_by = serializers.StringRelatedField(many=True)
    class Meta:
        model = Product
        fields = ['prod_name', 'sold_by', 'total_quantity']
        read_only_fields = ['prod_name', 'sold_by', 'total_quantity']


class VendorProductSerializer(serializers.ModelSerializer):
    prod_id = serializers.StringRelatedField()
    vendor_id = serializers.StringRelatedField()

    class Meta:
        model = VendorProduct
        fields = ['prod_id', 'vendor_id', 'unit_cost', 'quantity_left']
        read_only_fields = ['prod_id', 'vendor_id']


class CartProductSerializer(serializers.ModelSerializer):
    cart = serializers.StringRelatedField()
    product = serializers.StringRelatedField()

    class Meta:
        model = CartProduct
        fields = ['cart', 'product', 'quantity_wanted']
        read_only_fields = ['cart', 'product']
