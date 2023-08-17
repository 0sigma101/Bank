from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
    path("<int:Customer_id>",views.Customer_Check, name='detail'),
]

