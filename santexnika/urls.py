from django.contrib import admin
from django.urls import path, include
from accounts.views import home, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('clients/', include('clients.urls')),
    path('products/', include('products.urls')),
    path('sell/', include('sell.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
