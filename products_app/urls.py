from django.urls import path
from products_app.views import ProductView ,product_create_view,product_details_view,product_List_view,product_update_view,product_delete_view,product_mixin_view
urlpatterns = [
    # path('', ProductView.as_view(), name='products'),
    # path('<int:pk>', product_alt_view, name='productsdetails'),
    # path('<int:pk>/', product_mixin_view, name='productsdetails'),
    path('<int:pk>', product_details_view, name='productsdetails'),
    path('<int:pk>/update/', product_update_view, name='product_update_view'),
    path('<int:pk>/destroy/', product_delete_view, name='product_delete_view'),
    # path('', product_alt_view, name='productcreate'),
    path('create/', product_create_view, name='productcreate'),
    # path('', product_mixin_view, name='product_mixin_view'),
    path('', product_List_view, name='productList'),

]
