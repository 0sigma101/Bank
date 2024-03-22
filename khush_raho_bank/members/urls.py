from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.loginsignup, name='loginsignup'),
    path('members/details/<int:id>', views.details, name='details'),
    path('members/loginprocess', views.loginprocess, name='loginprocess'),
    path('members/signupprocess', views.signupprocess, name='signupprocess'),
]