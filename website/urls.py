from django.urls import path
from . import views

urlpatterns = [
   path("", views.home, name="home"),
   path("about/", views.about, name="about"),
   path("contact/", views.contact, name="contact"),
   path("ice-creams/", views.ice_creams, name="ice_creams"),
   path("ice-creams/<int:ice_cream_id>/", views.ice_cream_detail, name="ice_cream_detail"),
   path("add-to-cart/<int:ice_cream_id>/", views.add_to_cart, name="add_to_cart" ),
   path("remove_from_cart/<int:cart_item_id>/", views.remove_from_cart, name="remove_from_cart"),
   path("cart", views.cart_view, name="cart")
]
