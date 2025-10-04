from django.urls import path
from .views import client_list, client_create, client_view, client_edit, client_delete

urlpatterns = [
    path('', client_list, name='clientlist'),
    path('create/', client_create, name='clientcreate'),
    path('<int:id>/', client_view, name='clientview'),
    path('<int:id>/edit/', client_edit, name='clientedit'),
    path('<int:id>/delete/', client_delete, name='clientdelete'),
]