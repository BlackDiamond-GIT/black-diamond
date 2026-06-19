from django.urls import path
from . import views
from apps.contact.views import ContactPageView

app_name = 'pages'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('o-nas/', views.AboutView.as_view(), name='about'),
    path('pravidla-salonu/', views.SalonRulesView.as_view(), name='salon_rules'),
    path('soukromi/', views.PrivacyView.as_view(), name='privacy'),
    path('cenik/', views.PricesView.as_view(), name='prices'),
    path('caste-otazky/', views.FaqView.as_view(), name='faq'),
    path('kontakty/', ContactPageView.as_view(), name='contact'),
]
