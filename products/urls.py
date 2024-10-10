from django.urls import path
from .views import bulk_insert_products

urlpatterns = [
    path('bulk-insert/', bulk_insert_products, name='bulk_insert_products'),
]