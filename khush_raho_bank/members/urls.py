from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginsignup, name='loginsignup'),
    path('details/<int:id>', views.details, name='details'),
    path('loginprocess', views.loginprocess, name='loginprocess'),
    path('signupprocess', views.signupprocess, name='signupprocess'),
    path('chngpswd',views.chngpswd,name='chngpswd')
]