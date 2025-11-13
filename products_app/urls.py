from django.urls import path
from products_app.views import ProductView ,product_create_view,product_details_view,product_List_view,product_alt_view

urlpatterns = [
    # path('', ProductView.as_view(), name='products'),
    path('<int:pk>', product_alt_view, name='productsdetails'),
    # path('<int:pk>', product_details_view, name='productsdetails'),
    path('', product_alt_view, name='productcreate'),
    # path('create/', product_create_view, name='productcreate'),
    # path('', product_List_view, name='productList'),

]
