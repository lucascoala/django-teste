from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Contribuicoes
from django.views.generic import DetailView, TemplateView, View
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils import timezone
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, TruncMonth
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json
from django.core.exceptions import PermissionDenied


class ContribuicoesCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Tesoureiros", u"Secretária", u"Pastor"
    model = Contribuicoes
    fields = ['membro', 'valor', 'codigo', 'tipo_transferencia', 'data', 'descricao']
    template_name = 'contribuicoes/form.html'
    success_url = reverse_lazy('listar-contribuicoes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastrar contribuição"
        context['botao'] = "Cadastrar"
        
        return context

class ContribuicoesUpdade(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Tesoureiros", u"Secretária", u"Pastor"
    model = Contribuicoes
    fields = ['membro', 'valor', 'codigo', 'tipo_transferencia', 'data', 'descricao']
    template_name = 'contribuicoes/form.html'
    success_url = reverse_lazy('listar-contribuicoes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Editar contribuição"
        context['botao'] = "Salvar"
        
        return context

class ContribuicoesDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Tesoureiros", u"Secretária", u"Pastor"
    model = Contribuicoes
    template_name = 'contribuicoes/form-excluir.html'
    success_url = reverse_lazy('listar-contribuicoes')

class ContribuicoesList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Tesoureiros", u"Pastor", u"Secretaria"
    model = Contribuicoes
    template_name = 'contribuicoes/listas/contribuicoes-list.html'
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if not request.user.perfil.acesso_contribuicoes:
            raise PermissionDenied("Você não tem permissão para acessar este módulo.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        txt_nome = self.request.GET.get('data')
        if txt_nome:
            contribuicoes = Contribuicoes.objects.filter(data__icontains=txt_nome)
        else:
            contribuicoes = Contribuicoes.objects.all()
        return contribuicoes

class ContribuicoesView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Tesoureiros", u"Pastor", u"Secretaria"
    template_name = 'contribuicoes/visualizar.html'
    model = Contribuicoes
    context_object_name = 'contribuicoes'

class RelatorioMensalView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Tesoureiros", u"Pastor", u"Secretaria"
    model = Contribuicoes
    template_name = 'contribuicoes/listas/relatorio-mensal.html'
    context_object_name = 'contribuicoes'

    def get_queryset(self):
        return Contribuicoes.objects.filter(data__month=timezone.now().month)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tiporelatorio'] = "mensal"
        context['total_valor'] = self.get_queryset().aggregate(total=Sum('valor'))['total'] or 0
        return context    

class RelatorioDiarioView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Tesoureiros", u"Pastor", u"Secretaria" 
    model = Contribuicoes
    template_name = 'contribuicoes/listas/relatorio-mensal.html'
    context_object_name = 'contribuicoes'

    def get_queryset(self):
        return Contribuicoes.objects.filter(data=timezone.now().date())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tiporelatorio'] = "diário"
        context['total_valor'] = self.get_queryset().aggregate(total=Sum('valor'))['total'] or 0
        return context  

class RelatorioAnualView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Tesoureiros", u"Pastor", u"Secretaria" 
    model = Contribuicoes
    template_name = 'contribuicoes/listas/relatorio-mensal.html'
    context_object_name = 'contribuicoes'

    def get_queryset(self):
        return Contribuicoes.objects.filter(data__year=timezone.now().year)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tiporelatorio'] = "anual"
        context['total_valor'] = self.get_queryset().aggregate(total=Sum('valor'))['total'] or 0
        return context  


class PaginaInicial(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Tesoureiros", u"Pastor", u"Secretaria"
    template_name = "contribuicoes/listas/inicial-contribuicoes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcula totais
        hoje = timezone.now().date()
        
        # Total diário
        total_diario = Contribuicoes.objects.filter(
            data=hoje
        ).aggregate(
            total=Sum('valor')
        )['total'] or 0

        # Total mensal
        total_mensal = Contribuicoes.objects.filter(
            data__month=hoje.month,
            data__year=hoje.year
        ).aggregate(
            total=Sum('valor')
        )['total'] or 0

        # Total anual
        total_anual = Contribuicoes.objects.filter(
            data__year=hoje.year
        ).aggregate(
            total=Sum('valor')
        )['total'] or 0

        context['total_diario'] = total_diario
        context['total_mensal'] = total_mensal
        context['total_anual'] = total_anual
        
        return context

class ContribuicoesGraficoView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Tesoureiros", u"Pastor", u"Secretaria"
    template_name = 'contribuicoes/graficos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            # Dados para o gráfico mensal
            ano_atual = timezone.now().year
            contribuicoes_por_mes = Contribuicoes.objects.filter(
                data__year=ano_atual
            ).annotate(
                mes=TruncMonth('data')
            ).values('mes').annotate(
                total=Sum('valor')
            ).order_by('mes')

            # Preparar dados para os gráficos
            meses_pt = {
                1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
                5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
                9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
            }

            dados_mensais = []
            total_anual = 0

            # Garantir que todos os meses estejam representados
            for mes in range(1, 13):
                valor_mes = 0
                for contrib in contribuicoes_por_mes:
                    if contrib['mes'].month == mes:
                        try:
                            valor_mes = float(contrib['total'])
                            total_anual += valor_mes
                        except (ValueError, TypeError):
                            valor_mes = 0
                
                dados_mensais.append({
                    'mes': meses_pt[mes],
                    'valor': valor_mes
                })

            # Dados para o gráfico por tipo de transferência
            contribuicoes_por_tipo = Contribuicoes.objects.values(
                'tipo_transferencia'
            ).annotate(
                total=Sum('valor')
            ).order_by('tipo_transferencia')

            dados_tipos = []
            for tipo in contribuicoes_por_tipo:
                try:
                    valor = float(tipo['total'])
                except (ValueError, TypeError):
                    valor = 0
                
                dados_tipos.append({
                    'tipo': tipo['tipo_transferencia'],
                    'valor': valor
                })

            # Converter para JSON com tratamento de erros
            context['dados_mensais'] = json.dumps(dados_mensais)
            context['dados_tipos'] = json.dumps(dados_tipos)
            context['total_anual'] = total_anual

            # Adicionar estatísticas adicionais
            context['total_mes_atual'] = sum(
                float(c['total']) for c in contribuicoes_por_mes.filter(
                    mes__month=timezone.now().month
                )
            ) if contribuicoes_por_mes.exists() else 0

            # Média mensal
            meses_com_contribuicao = contribuicoes_por_mes.count()
            context['media_mensal'] = total_anual / meses_com_contribuicao if meses_com_contribuicao > 0 else 0

        except Exception as e:
            # Em caso de erro, fornecer dados vazios
            context['dados_mensais'] = json.dumps([])
            context['dados_tipos'] = json.dumps([])
            context['total_anual'] = 0
            context['total_mes_atual'] = 0
            context['media_mensal'] = 0
            context['erro'] = str(e)

        return context



class ResumoFinanceiroView(TemplateView):
    template_name = 'contribuicoes/listas/inicial-contribuicoes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = timezone.now().date()
        mes_atual = hoje.month
        ano_atual = hoje.year

        # Total mensal
        total_mensal = Contribuicoes.objects.filter(data__month=mes_atual, data__year=ano_atual).aggregate(Sum('valor'))['valor__sum'] or 0

        # Cálculo de 10% e 5%
        ipb_percentual = total_mensal * 0.10
        presbiterio_percentual = total_mensal * 0.05

        context['total_mensal'] = total_mensal
        context['ipb_percentual'] = ipb_percentual
        context['presbiterio_percentual'] = presbiterio_percentual
        return context
        