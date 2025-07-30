from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from .models import Despesas
from contribuicoes.models import Contribuicoes
from django.db.models import Sum, Count  # Added Count here
from django.db.models.functions import TruncMonth
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar
from .forms import DespesasForm
from decimal import Decimal

class DespesasCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria", u"Pastor", u"Tesoureiro"
    model = Despesas
    form_class = DespesasForm
    template_name = 'despesas/form.html'
    success_url = reverse_lazy('listar-despesas')

    def form_valid(self, form):
        form.instance.usuario_cadastro = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastrar Despesa"
        context['botao'] = "Cadastrar"
        return context

class DespesasList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Pastor", u"Secretaria", u"Tesoureiro"
    model = Despesas
    template_name = 'despesas/listas/despesas_list.html'
    paginate_by = 10


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Você precisa estar autenticado para acessar este módulo.")

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if not hasattr(request.user, 'perfil'):
            raise PermissionDenied("Seu perfil não está configurado corretamente.")

        if not request.user.perfil.acesso_despesas:
            raise PermissionDenied("Você não tem permissão para acessar este módulo.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        mes = self.request.GET.get('mes')
        ano = self.request.GET.get('ano')
        status = self.request.GET.get('status')
        
        if mes and ano:
            queryset = queryset.filter(data_vencimento__month=mes, 
                                     data_vencimento__year=ano)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        context['total_despesas'] = queryset.aggregate(
            total=Sum('valor'))['total'] or 0
        context['total_pagas'] = queryset.filter(
            status='Pago').aggregate(total=Sum('valor'))['total'] or 0
        context['total_pendentes'] = queryset.filter(
            status='Pendente').aggregate(total=Sum('valor'))['total'] or 0
            
        return context

class DespesasUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria", u"Pastor", u"Tesoureiro"
    model = Despesas
    form_class = DespesasForm
    template_name = 'despesas/form.html'
    success_url = reverse_lazy('listar-despesas')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Editar Despesa"
        context['botao'] = "Salvar"
        return context

class DespesasDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria", u"Pastor", u"Tesoureiro"
    model = Despesas
    template_name = 'despesas/form-excluir.html'
    success_url = reverse_lazy('listar-despesas')

class PanoramaFinanceiroView(LoginRequiredMixin, TemplateView):  # Changed from PanoramaFinanceiro
    template_name = 'despesas/panorama_financeiro.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current year and month
        hoje = datetime.now()
        ano = self.request.GET.get('ano', hoje.year)
        mes = self.request.GET.get('mes', hoje.month)
        
        # Get available years from despesas
        anos_disponiveis = Despesas.objects.dates('data_vencimento', 'year').values_list('data_vencimento__year', flat=True)
        if not anos_disponiveis:
            anos_disponiveis = [hoje.year]
        
        # Filter despesas by month and year
        despesas = Despesas.objects.filter(
            data_vencimento__year=ano,
            data_vencimento__month=mes
        )

        # Group by CLC instead of categoria
        despesas_por_categoria = despesas.values('clc').annotate(
            total=Sum('valor'),
            quantidade=Count('id')
        ).order_by('clc')

        # Add description for each CLC
        for item in despesas_por_categoria:
            clc_code = item['clc']
            # Get the display name from the model choices
            clc_dict = dict(Despesas.DESPESAS_CHOICES)
            item['descricao'] = clc_dict.get(clc_code, 'Desconhecido')

        context['despesas_por_categoria'] = despesas_por_categoria
        context['ano'] = ano
        context['mes'] = mes
        context['anos_disponiveis'] = anos_disponiveis
        context['mes_atual'] = mes
        context['ano_atual'] = ano
        
        return context