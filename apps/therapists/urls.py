from django.urls import path
from . import views

app_name = 'therapists'

urlpatterns = [
    path('', views.TherapistListView.as_view(), name='list'),
    path('<slug:slug>/', views.TherapistDetailView.as_view(), name='detail'),
]
