from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render

from eCartApp.exceptions import *
from eCartApp.models import Cart, Customer, Product, Vendor, VendorProduct, CartProduct
from eCartApp.serializers import CartSerializer, CustomerSerializer, ProductSerializer, VendorSerializer, VendorProductSerializer, CartProductSerializer

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView



# Create your views here.
class CustomerList(APIView):
    """ Retrieve list of  all registered customers or register a new one """
    # 'GET'
    def get(self, request,format=None):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many = True)
        return Response(serializer.data)

    # 'POST'
    def post(self, request, format=None):
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            # save Customer data if valid
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        # if not valid, return error
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class CustomerInd(APIView):
    """ Retrieve the information of a single customer or update/delete his/her information """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_customer(self, email):
        try:
            return Customer.objects.get(email_id = email)
        except Customer.DoesNotExist:
            raise NoCustomersFoundException(email)

    # 'GET'
    def get(self, request, email, format=None):
        cust = self.get_customer(email)
        serializer = CustomerSerializer(cust)
        return Response(serializer.data)

    # 'PUT'
    def put(self, request, email, format=None):
        cust = self.get_customer(email)
        serializer = CustomerSerializer(cust,data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 'DELETE'
    def delete(self, request, email, format = None):
        cust = self.get_customer(email)
        cust.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


""" I don't think getting the information of carts is useful? Better to get information on a customer and his/her cart instead... """
# class CartList(APIView):
#     """ Retrieve list of all carts and basic information """
#     # 'GET'
#     def get(self, request, format=None):
#         carts = Cart.objects.all()
#         serializer = CartSerializer(carts, many=True)
#         return Response(serializer.data)
#
#
#
class CartInd(APIView):
    """ Retrieve single cart of specific customer """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_cart_by_user(self, user_email):
        try:
            return Cart.objects.get(customer__email_id=user_email)
        except Cart.DoesNotExist:
            raise NoCustomersFoundException(user_email)

    # 'GET'
    def get(self, request, email, format=None):
        cart = self.get_cart_by_user(email)
        serializer = CartSerializer(cart)
        return Response(serializer.data)



class ProductList(APIView):
    """ Retrieve list of all products being sold """
    # 'GET'
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



class ProductInd(APIView):
    """ Retrieve information on products based on search query """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_products_by_name(self, p_name):
        p = Product.objects.filter(prod_name__contains=p_name)
        if len(p) == 0:
            raise NoProductsFoundException(p_name)
        else:
            return p

    # 'GET'
    def get(self, request, name='', format=None):
        products = self.get_products_by_name(p_name=name)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



class VendorList(APIView):
    """ Retrieve all registered vendors or register a new one """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # 'GET'
    def get(self, request, name='', format = None):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    # 'POST'
    def post(self, request, format = None):
        serializer = VendorSerializer(data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorInd(APIView):
    """ Retrieve the information of a single vendor or update/delete his/her information """

    def get_vendor(self, email):
        try:
            return Vendor.objects.get(vendor_email__iexact=email)
        except Vendor.DoesNotExist:
            raise NoVendorsFoundException(email)

    # 'GET'
    def get(self, request, email, format=None):
        vendor = self.get_vendor(email)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    # 'PUT'
    def put(self, request, email, format=None):
        vendor = self.get_vendor(email)
        serializer = VendorSerializer(vendor,data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 'DELETE'
    def delete(self, request, email, format=None):
        curr_vendor = self.get_vendor(email)
        curr_vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class VendorProductList(APIView):
    """ Retrieve more specific information on products being sold by vendors or add a new product"""
    def get_vendor(self, email):
        try:
            return Vendor.objects.get(vendor_email__iexact=email)
        except Vendor.DoesNotExist:
            raise NoVendorsFoundException(email)

    def check_existing_product(self, name):
        try:
            p = Product.objects.get(prod_name__iexact=name)
            return p
        except Product.DoesNotExist:
            return None

    def get(self, request, format=None):
        vps = VendorProduct.objects.all()
        serializer = VendorProductSerializer(vps, many = True)
        return Response(serializer.data)

    # 'POST' a new vendor product
    def post(self, request, format=None):
        # set up variables for readability
        prod_name = request.data['prod_name']
        vendor_email = request.data['vendor_email']
        unit_cost = request.data['unit_cost']
        quantity = request.data['quantity']


        # create new product to add
        prod = self.check_existing_product(name = prod_name)
        curr_vendor = self.get_vendor(vendor_email)
        if not prod:
            prod = Product.objects.create(prod_name = prod_name)

        prod.sold_by.add(curr_vendor)

        # create new vendor product and add
        try:
            vp_data = VendorProduct.objects.create(unit_cost = unit_cost, quantity_left = quantity)
            vp_data.prod_id, vp_data.vendor_id = prod, curr_vendor
            vp_data.save()
            serializer = VendorProductSerializer(data = vp_data.__dict__)
            if serializer.is_valid():
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            vp_data.delete()
            raise VendorProductPairNotUniqueException(vendor_email)



class VendorProductInd(APIView):
    """ Retrieve information on a vendor's product or update/delete product information """

    def get_vendor_product(self, email, p_name):
        try:
            v = Vendor.objects.get(vendor_email__iexact=email)
            p = v.products_to_sell.all().get(prod_id__prod_name__iexact = p_name)
            return p
        except Vendor.DoesNotExist:
            raise NoVendorsFoundException(email)
        except VendorProduct.DoesNotExist:
            raise VendorNotSellingException(email)

    def get(self, request, email, p_name, format=None):
        curr_vprod = self.get_vendor_product(email, p_name)
        serializer = VendorProductSerializer(curr_vprod)
        return Response(serializer.data)

    def put(self, request, email, p_name, format=None):
        curr_vprod = self.get_vendor_product(email, p_name)
        serializer = VendorProductSerializer(curr_vprod, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, email, p_name, format=None):
        curr_vprod = self.get_vendor_product(email, p_name)
        curr_vprod.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CartProductList(APIView):
    """ Retrieve list of all products that have been added to carts or add a new product """

    def get_cart_by_user(self, user_email):
        try:
            return Cart.objects.get(customer__email_id=user_email)
        except Cart.DoesNotExist:
            raise NoCustomersFoundException(user_email)

    def get(self, request, format = None):
        prods = CartProduct.objects.all()
        serializer = CartProductSerializer(prods, many=True)
        return Response(serializer.data)

    # 'POST' new vendor product
    def post(self, request, format = None):
        # get vendor product related to input
        try:
            curr_cust = request.data['cust_email']
            vendor_email = request.data['vendor_email']
            prod_name = request.data['prod_name']
            quantity_wanted = request.data['quantity_wanted']

            prod = VendorProduct.objects.get(vendor_id__vendor_email__iexact = vendor_email, prod_id__prod_name__iexact = prod_name)

            if prod.quantity_left < quantity_wanted:
                raise NotEnoughProductsException()

            cart = self.get_cart_by_user(curr_cust)
            cp_data = CartProduct.objects.create(cart = cart, product = prod, quantity_wanted = quantity_wanted)

        except ObjectDoesNotExist:
            raise VendorNotSellingException(vendor_email)

        except IntegrityError:
            raise ProductAlreadyInCartException(prod_name)



class CartProductInd(APIView):
    """ Retrieve information on a product added to specific cart or update/delete product information """

    def get_cart_prod(self, c_email, v_email, p_name):
        try:
            c = Cart.objects.get(customer__email_id__iexact = c_email)
            p = c.products_in_cart.all().filter(product__prod_id__prod_name__iexact = p_name)
            cp = p.get(product__vendor_id__vendor_email__iexact = v_email)
            return cp

        except Cart.DoesNotExist:
            raise NoCustomersFoundException(c_email)

        except CartProduct.DoesNotExist:
            raise CartProductDoesNotExistException(c_email)

    def get(self, request, c_email, v_email, p_name, format=None):
        cart_prod = self.get_cart_prod(c_email, v_email, p_name)
        serializer = CartProductSerializer(cart_prod)
        return Response(serializer.data)

    def put(self, request, c_email, v_email, p_name, format=None):
        curr_cprod = self.get_cart_prod(c_email, v_email, p_name)
        quant_left, quant_wanted = curr_cprod.product.quantity_left, request.data['quantity_wanted']
        serializer = CartProductSerializer(curr_cprod, data = request.data, partial = True)
        if serializer.is_valid():
            if quant_left < quant_wanted:
                raise NotEnoughProductsException(v_email)
            if quant_wanted < 0:
                raise NegativeQuantityException()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, c_email, v_email, p_name, format=None):
        cart_prod = self.get_cart_prod(c_email, v_email, p_name)
        cart_prod.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



""" Example Authentication """
class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': "asdfafdsaf"
        }
        return Response(content)
