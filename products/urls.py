from django.urls import path
from .views import statistics_view, product_list, product_create, product_view, product_edit, product_delete, check_existing_product, update_existing_product, product_import, process_import, export_products_excel

urlpatterns = [
    path('', product_list, name='productlist'),
    path('create/', product_create, name='productcreate'),
    path('import/', product_import, name='productimport'),
    path('import/process/', process_import, name='process_import'),
    path('check-existing/', check_existing_product, name='check_existing_product'),
    path('update-existing/', update_existing_product, name='update_existing_product'),
    path('<int:id>/', product_view, name='productview'),
    path('<int:id>/edit/', product_edit, name='productedit'),
    path('<int:id>/delete/', product_delete, name='productdelete'),
    path('export/', export_products_excel, name='product_export'),

    path('statistics/', statistics_view, name='statistics')
]