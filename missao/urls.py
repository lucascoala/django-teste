from django.urls import path
from .views import MissaoCreate, MissaoList, MissaoUpdate, MissaoDelete, MissaoView

urlpatterns = [
    path('cadastrar/', MissaoCreate.as_view(), name='cadastrar-missao'),
    path('listar/missoes', MissaoList.as_view(), name='listar-missoes'),
    path('editar/<int:pk>/', MissaoUpdate.as_view(), name='editar-missao'),
    path('excluir/<int:pk>/', MissaoDelete.as_view(), name='excluir-missao'),
    path('ver/<int:pk>/', MissaoView.as_view(), name='ver-missao'),
]