from django.urls import path
from .views import *

app_name = "leads"

urlpatterns = [
    #path('',lead_list, name = 'lead-list'),
    path('',LeadListView.as_view(), name = 'lead-list'),
    #path('<int:pk>/',lead_detail, name = 'lead-detail'),# int is written to run this url if and only if pk is integer.
    path('<int:pk>/',LeadDetailView.as_view(), name = 'lead-detail'),
    #path('<int:pk>/update/',lead_update, name = 'lead-update'),
    path('<int:pk>/update/',LeadUpdateView.as_view(), name = 'lead-update'),
    #path('<int:pk>/delete/',lead_delete, name = 'lead-delete'),
    path('<int:pk>/delete/',LeadDeleteView.as_view(), name = 'lead-delete'),
    # Assign agent
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name = 'assign-agent'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name = 'lead-category-update'),
    #path('create-a-new-lead/', lead_create, name = 'lead-create'),
    path('create/', LeadCreateView.as_view(), name = 'lead-create'),
    path('categories/',CategoryListView.as_view(), name = 'category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('create-category/', CategoryCreateView.as_view(), name='category-create'),
]