from django.urls import path
from .views import lead_list, lead_detail, lead_create

app_name = "leads"

urlpatterns = [
    path('',lead_list),
    path('<int:pk>/',lead_detail),# int is written to run this url if and only if pk is integer.
    path('create', lead_create)
]