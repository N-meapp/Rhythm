from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index,),
    path('events/', views.Events,name='events'),
    path('book/', views.booking_form, name='booking_form'),
    path('book/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # Updated: removed user_id requirement
    path('login/<int:user_id>/', views.login_view, name='login_with_id'),  # Keep this pattern for after registration
    path('logout/', views.logout_view, name='logout'),
     path('about/', views.about, name='about'),
    

]