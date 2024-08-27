from django.urls import path
from . import views

urlpatterns = [
   path("", views.home, name="home"),
   path("about/", views.about, name="about"),
   path("contact/", views.contact, name="contact"),
   path("ice-creams/", views.ice_creams, name="ice_creams"),
   path("ice-creams/<int:ice_cream_id>/", views.ice_cream_detail, name="ice_cream_detail"),
]
