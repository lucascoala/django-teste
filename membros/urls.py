from django.urls import path
from .views import MembrosCreate, MembrosUptade, MembrosDelete, MembrosList, MembrosView, GerarPDFMembros, DashboardView, exportar_membros_excel

urlpatterns = [
   # path('endereço/', MinhaView.as_view(), name = "Nome-da-url"),
   path('cadastrar/membros/', MembrosCreate.as_view(), name = "cadastrar-membros"),
   path('editar/membros/<int:pk>/', MembrosUptade.as_view(), name = 'editar-membros'),
   path('excluir/membros/<int:pk>/', MembrosDelete.as_view(), name = 'excluir-membros'),
   path('visualizar/membros/<int:pk>/', MembrosView.as_view(), name = 'visualizar-membro'),
   path('listar/membros/', MembrosList.as_view(), name = 'listar-membros'),
   path('exportar-excel/', exportar_membros_excel, name='exportar_membros_excel'),
   path('gerar-pdf/', GerarPDFMembros.as_view(), name='gerar-pdf-membros'),
   path('dashboard/', DashboardView.as_view(), name='dashboard-membros'),
]