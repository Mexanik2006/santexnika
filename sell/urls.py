from django.urls import path
from .views import sale_create, sale_list, sale_detail, sale_receipt, sale_qr_code, get_client_discount, get_product_info

urlpatterns = [
    path('', sale_list, name='sale_list'),
    path('create/', sale_create, name='sale_create'),
    path('<int:id>/', sale_detail, name='sale_detail'),
    path('<int:id>/receipt/', sale_receipt, name='sale_receipt'),
    path('<int:id>/qr/', sale_qr_code, name='sale_qr_code'),
    path('get-client-discount/', get_client_discount, name='get_client_discount'),
    path('get-product-info/', get_product_info, name='get_product_info'),
]