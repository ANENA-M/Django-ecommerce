from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    
    path('',views.index,name='home'),
    path('list_products/',views.list_products, name='list_products'),
    path('products_details/<pk>',views.products_details,name='products_details')
]

