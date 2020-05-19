from rest_framework.exceptions import APIException

class NoCustomersFoundException(APIException):
    def __init__(self, email):
        APIException.__init__(self, "No customers exist with email \'%s\'" % email, "no_customers")
    status_code = 404

class NoProductsFoundException(APIException):
    def __init__(self, name):
        APIException.__init__(self, "Could not find product that contains \'%s\'" % name)
    status_code = 404

class NoCartFoundException(APIException):
    def __init__(self, name):
        APIException.__init__(self, "Could not find cart for customer that contains \'%s\'" % name)
    status_code = 404

class NoVendorsFoundException(APIException):
    def __init__(self, email):
        APIException.__init__(self, "No vendors exist with email \'%s\'" % email)
    status_code = 404

class ProductAlreadyExistsException(APIException):
    def __init__(self, name):
        APIException.__init__(self, "Product \'%s\' seems to already exist. Update the existing product or add a new one!" % name)
    status_code = 404

class CartProductDoesNotExistException(APIException):
    def __init__(self, email):
        APIException.__init__(self, "Customer \'%s\' does not have specified product in cart!" % email)
    status_code = 404

class VendorProductPairNotUniqueException(APIException):
    def __init__(self, email):
        APIException.__init__(self, "Vendor \'%s\' is already selling that product!" % email)
    status_code = 404

class NotEnoughProductsException(APIException):
    def __init__(self, email):
        APIException.__init__(self, "Vendor \'%s\' does not have that many units to sell!" % email)
    status_code = 404

class NegativeQuantityException(APIException):
    def __init__(self):
        APIException.__init__(self, "Quantity must be a nonnegative integer!")
    status_code = 404

class VendorNotSellingException(APIException):
    def __init__(self, email):
        APIException.__init__(self, "Vendor \'%s\' is not selling that item!" % email)
    status_code = 404

class ProductAlreadyInCartException(APIException):
    def __init__(self, name):
        APIException.__init__(self, "Product \'%s\' already exists in cart!" % name)
    status_code = 404

class SpecifyQuantityException(APIException):
    def __init__(self):
        APIException.__init__(self, "You must specify a quantity!")
    status_code = 404
