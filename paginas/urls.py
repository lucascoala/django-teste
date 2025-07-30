from django.urls import path
from .views import IndexView, SobreView, PoliticaPrivacidadeView, TermosUsoView, ConsentimentoView, SalvarConsentimentoView

urlpatterns = [    
    path('', IndexView.as_view(), name='index'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('politica-privacidade/', PoliticaPrivacidadeView.as_view(), name='politica-privacidade'),
    path('termos-uso/', TermosUsoView.as_view(), name='termos-uso'),
    path('consentimento/', ConsentimentoView.as_view(), name='consentimento'),
    path('salvar-consentimento/', SalvarConsentimentoView.as_view(), name='salvar-consentimento'),
]