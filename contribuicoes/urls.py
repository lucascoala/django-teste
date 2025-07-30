from django.urls import path
from .views import ResumoFinanceiroView
from .views import (
    ContribuicoesCreate, 
    ContribuicoesUpdade, 
    ContribuicoesDelete, 
    ContribuicoesList, 
    ContribuicoesView, 
    RelatorioMensalView, 
    RelatorioDiarioView, 
    RelatorioAnualView,
    PaginaInicial, 
    ContribuicoesGraficoView,
    
)

urlpatterns = [
   # path('endereço/', MinhaView.as_view(), name = "Nome-da-url"),
   path('cadastrar/contribuicoes/', ContribuicoesCreate.as_view(), name = "cadastrar-contribuicoes"),
   path('editar/contribuicoes/<int:pk>', ContribuicoesUpdade.as_view(), name =  'editar-contribuicoes'),
   path('excluir/contribuicoes/<int:pk>', ContribuicoesDelete.as_view(), name =  'excluir-contribuicoes'),
   path('listar/contribuicoes/', ContribuicoesList.as_view(), name =  'listar-contribuicoes'),
   path('visualizar/contribuicoes/<int:pk>', ContribuicoesView.as_view(), name =  'visualizar-contribuicoes'),
   path('relatorio/mensal/', RelatorioMensalView.as_view(), name='relatorio-mensal'),
   path('relatorio/diario/', RelatorioDiarioView.as_view(), name='relatorio-diario'),
   path('relatorio/anual/', RelatorioAnualView.as_view(), name='relatorio-anual'),
   path('inicial/contribuicoes/', PaginaInicial.as_view(), name="paginaInicial-contribuicoes"),
   path('graficos/', ContribuicoesGraficoView.as_view(), name='contribuicoes-graficos'),
   path('', ResumoFinanceiroView.as_view(), name='paginaInicial-contribuicoes'),
   
]
