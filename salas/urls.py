from django.urls import path
from .views import SalasCreate, SalasList, SalasUpdate, SalasDelete, SalasView, GerarPDFSalas
from .views_ajax import buscar_alunos

urlpatterns = [
    path('buscar-alunos/', buscar_alunos, name='buscar-alunos'),
    path('Salas/', SalasCreate.as_view(), name='salas-list'),
    path('', SalasList.as_view(), name='listar-salas'),
    path('editar/<int:pk>/', SalasUpdate.as_view(), name='editar-sala'),
    path('excluir/<int:pk>/', SalasDelete.as_view(), name='excluir-sala'),
    path('ver/<int:pk>/', SalasView.as_view(), name='ver-sala'),
    path('gerar_pdf/', GerarPDFSalas.as_view(), name='gerar-pdf-salas'),
    path('cadastrar/', SalasCreate.as_view(), name='cadastrar-sala'),  # Adicionando a URL para cadastrar-sala
]
