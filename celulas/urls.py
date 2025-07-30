from django.urls import path
from .views import CelulasCreate, CelulasUpdade, CelulasDelete, CelulasList, CelulasView, GerarPDFCelulas

urlpatterns = [
   # path('endereço/', MinhaView.as_view(), name = "Nome-da-url"),
   path('cadastrar/celulas', CelulasCreate.as_view(), name = "cadastrar-celulas"),
   path('editar/celulas/<int:pk>', CelulasUpdade.as_view(), name =  'editar-celulas'),
   path('excluir/celulas/<int:pk>', CelulasDelete.as_view(), name =  'excluir-celulas'),
   path('visualizar/celulas/<int:pk>', CelulasView.as_view(), name =  'visualizar-celulas'),
   path('listar/celulas', CelulasList.as_view(), name =  'listar-celulas'),
   path('gerar-pdf/', GerarPDFCelulas.as_view(), name='gerar-pdf-celulas'),
]
