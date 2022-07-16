
from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.product_list, name='product_list'),
    path('productdetail/<int:product_id>',
         views.productdetail, name='productdetail'),
    path('addtocart', views.add_to_cart, name='addtocart'),
    path('checkout', views.checkout, name='checkout'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('address', views.address, name='address'),
    path('states_load', views.states_load, name='states-load'),
    path('country_load', views.country_load, name='country-load'),
    path('change_password', views.change_password, name='change_password'),
    path('logout', views.logout, name='logout'),
    path('seller_login', views.seller_login, name='seller_login'),
    path('seller_register', views.seller_register, name='seller_register'),
    path('seller_home', views.seller_home, name='seller_home'),
    path('seller_new_product', views.seller_new_product, name='seller_new_product'),
    path('seller_view_products', views.seller_view_products,
         name='seller_view_products'),
    path('seller_productdetail/<int:product_id>', views.seller_productdetail,
         name='seller_productdetail'),
    path('updatecart', views.updatecart, name='updatecart'),
    path('view_products/<str:category>/<str:sub_category>',
         views.view_products, name='view_products'),
    path('filter_load', views.filter_load, name='filter_load'),
    path('view_customized_products/<str:category>/<str:sub_category>', views.view_customized_products,
         name='view_customized_products'),
    path('select_an_address', views.select_an_address, name='select_an_address'),
    path('select_an_address_detailed/<str:type>/<str:product_id>/<str:size>',
         views.select_an_address_detailed, name='select_an_address_detailed'),
    path('select_an_address', views.select_an_address, name='select_an_address'),
    path('placeorder/<int:step>', views.placeorder, name='placeorder'),
    path('myorders', views.myorders, name='myorders'),
    path('get_cart_items', views.get_cart_items, name='get_cart_items'),
    path('seller_update_product/<int:product_id>', views.seller_update_product,
         name='seller_update_product')
]
