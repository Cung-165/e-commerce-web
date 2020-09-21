from django.urls import path
from . import views


urlpatterns = [
    path('',views.store,name="store"),
    path('cart/',views.Cart,name="Cart"),
    path('CheckOut/',views.CheckOut,name="CheckOut"),

    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name='process_order')
]
