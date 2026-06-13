from django.urls import path
from . import views

urlpatterns = [
    path('slots/', views.slots_fragment, name='slots'),
]
