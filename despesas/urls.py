from django.urls import path
from .views import (
    DespesasCreate, DespesasUpdate, DespesasDelete, 
    DespesasList, PanoramaFinanceiroView  # Changed from PanoramaFinanceiro
)
# Importação explícita e correta da view de relatórios
from .views_relatorios import RelatorioDespesasView

urlpatterns = [
    path('cadastrar/', DespesasCreate.as_view(), name='cadastrar-despesas'),
    path('editar/<int:pk>/', DespesasUpdate.as_view(), name='editar-despesas'),
    path('excluir/<int:pk>/', DespesasDelete.as_view(), name='excluir-despesas'),
    path('listar/', DespesasList.as_view(), name='listar-despesas'),
    path('panorama-financeiro/', PanoramaFinanceiroView.as_view(), name='panorama-financeiro'),
    path('relatorio-despesas/', RelatorioDespesasView.as_view(), name='relatorio-despesas'),
]