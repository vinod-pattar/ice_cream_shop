from django.urls import path
from . import views

urlpatterns = [
   path("", views.home, name="home"),
   path("about/", views.about, name="about"),
   path("contact/", views.contact, name="contact"),
   path("ice-creams/", views.ice_creams, name="ice_creams"),
   path("ice-creams/<int:ice_cream_id>/", views.ice_cream_detail, name="ice_cream_detail"),
   path("add-to-cart/<int:ice_cream_id>/", views.add_to_cart, name="add_to_cart" ),
   path("cart", views.cart_view, name="cart"),
   path("update-cart", views.update_cart, name="update_cart"),
   path("checkout", views.checkout, name="checkout"),
   path("payment/<int:order_id>/", views.payment, name="payment"),
   path("verify-payment/", views.verify_payment, name="verify_payment"),
   path("orders", views.orders_list, name="orders_list"),
   path("order_details/<int:order_id>/", views.order_details, name="order_details" ),
   path("cancel-order/<int:order_id>/", views.cancel_order, name="cancel_order"),
   path("addresses", views.addresses, name="addresses"),
   path("add-address", views.add_address, name="add_address"),
   path("edit-address/<int:address_id>/", views.edit_address, name="edit_address"),
   path("delete-address/<int:address_id>/", views.delete_address, name="delete_address"),
]
