from django.urls import path, include
from eCartApp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('customers/', views.CustomerList.as_view()),
    path('customers/<str:email>/', views.CustomerInd.as_view()),
    path('carts/<str:email>/', views.CartInd.as_view()),
    path('products/<str:name>/', views.ProductInd.as_view()),
    path('products/', views.ProductList.as_view()),
    path('vendors/', views.VendorList.as_view()),
    path('vendors/<str:email>/', views.VendorInd.as_view()),
    path('cartproducts/', views.CartProductList.as_view()),
    path('cartproducts/<str:c_email>/<str:v_email>/<str:p_name>/', views.CartProductInd.as_view()),
    path('vendorproducts/', views.VendorProductList.as_view()),
    path('vendorproducts/<str:email>/<str:p_name>/', views.VendorProductInd.as_view()),
    path('example/', views.ExampleView.as_view()),
    path('rest-auth/', include('rest_auth.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
