from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="Tracking"),
    path('search/', views.search, name="Search"),
    path('productview/<int:iden>', views.productView, name="Productview"),
    path('checkout/', views.checkout, name="Checkout"),
] 
