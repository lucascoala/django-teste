from django.urls import path
from .views import VisitantesCreate, VisitantesDelete, VisitantesList, VisitantesUpdade, VisitantesView

urlpatterns = [
   # path('endereço/', MinhaView.as_view(), name = "Nome-da-url"),
   path('cadastrar/visitantes', VisitantesCreate.as_view(), name = "cadastrar-visitantes"),
   path('editar/visitantes/<int:pk>', VisitantesUpdade.as_view(), name =  'editar-visitantes'),
   path('excluir/visitantes/<int:pk>', VisitantesDelete.as_view(), name =  'excluir-visitantes'),
   path('visualizar/visitantes/<int:pk>', VisitantesView.as_view(), name =  'visualizar-visitantes'),
   path('listar/visitantes', VisitantesList.as_view(), name =  'listar-visitantes'),
]
