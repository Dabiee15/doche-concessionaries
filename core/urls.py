from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('booking/', views.booking_view, name='booking'),
    path('booking/success/<int:pk>/', views.booking_success, name='booking_success'),
    path('manage/', views.manage_bookings, name='manage_bookings'),
    path('manage/booking/<int:pk>/edit/', views.edit_booking, name='edit_booking'),
]