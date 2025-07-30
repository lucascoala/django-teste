from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.db.models import Sum
from datetime import datetime
from .models import Despesas
import calendar

class RelatorioDespesasView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = 'login'
    group_required = u"Administradores", u"Secretaria", u"Pastor", u"Tesoureiro"
    model = Despesas
    template_name = 'despesas/relatorios/relatorio_despesas.html'
    paginate_by = None  # Desabilita paginação para o relatório

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        mes = self.request.GET.get('mes')
        ano = self.request.GET.get('ano')
        categoria = self.request.GET.get('categoria')
        status = self.request.GET.get('status')
        
        if mes and ano:
            queryset = queryset.filter(
                data_vencimento__month=mes,
                data_vencimento__year=ano
            )
        if categoria:
            queryset = queryset.filter(clc=categoria)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset.order_by('data_vencimento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        # Cálculos totais
        context['total_despesas'] = queryset.aggregate(
            total=Sum('valor'))['total'] or 0
        context['total_pagas'] = queryset.filter(
            status='Pago').aggregate(total=Sum('valor'))['total'] or 0
        context['total_pendentes'] = queryset.filter(
            status='Pendente').aggregate(total=Sum('valor'))['total'] or 0

        # Dados para filtros
        hoje = datetime.now()
        context['meses'] = [
            (i, calendar.month_name[i]) for i in range(1, 13)
        ]
        context['anos'] = range(hoje.year - 2, hoje.year + 2)
        context['categorias'] = Despesas.DESPESAS_CHOICES
        
        # Parâmetros selecionados
        mes = self.request.GET.get('mes')
        ano = self.request.GET.get('ano')
        categoria = self.request.GET.get('categoria')
        status = self.request.GET.get('status')
        
        context['mes'] = int(mes) if mes else ''
        context['ano'] = int(ano) if ano else hoje.year
        context['categoria'] = categoria
        context['status'] = status
        
        # Nomes para exibição
        if mes:
            context['mes_nome'] = calendar.month_name[int(mes)]
        if categoria:
            context['categoria_nome'] = dict(Despesas.DESPESAS_CHOICES).get(categoria)
            
        context['now'] = datetime.now()
        
        return context