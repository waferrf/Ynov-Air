from django.urls import path
from . import views

from .auth_views import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    profile_update_view
)

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_flights, name='search_flights'),
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('flight/<int:flight_id>/book/', views.booking_create, name='booking_create'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    # Authentification
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update_view, name='profile_update'),
    
    # Lost Objects
    path('lost-objects/', views.lost_objects_list, name='lost_objects_list'),
    path('lost-objects/<int:object_id>/', views.lost_object_detail, name='lost_object_detail'),
    path('lost-objects/report/', views.lost_object_report, name='lost_object_report'),
    path('lost-objects/<int:object_id>/claim/', views.lost_object_claim, name='lost_object_claim'),
    path('my-lost-objects/', views.my_lost_objects, name='my_lost_objects'),
]
