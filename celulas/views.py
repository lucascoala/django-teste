from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, View
from .models import Celulas
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from mysite.utils import render_to_pdf
from django.http import HttpResponse
from datetime import datetime
from django.core.exceptions import PermissionDenied

class CelulasCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Lideres", u"Secretaria", u"Pastor", u"Celulas"
    model = Celulas
    fields = ['lider', 'local', 'dia_semana', 'quant_visitantes', 'quant_membros', 'hora_incio', 'hora_fim', 'descricao']
    template_name = 'celulas/form.html'
    success_url = reverse_lazy('listar-celulas')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastro de celulas"
        context['botao'] = "Cadastrar"
        
        return context

class CelulasUpdade(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Lideres", u"Secretaria", u"Pastor"
    model = Celulas
    fields = ['lider', 'local', 'dia_semana', 'quant_visitantes', 'quant_membros', 'hora_incio', 'hora_fim', 'descricao']
    template_name = 'celulas/form.html'
    success_url = reverse_lazy('listar-celulas')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Editar celula"
        context['botao'] = "Salvar"
        
        return context

class CelulasDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Lideres", u"Secretaria", u"Pastor"
    model = Celulas
    template_name = 'celulas/form-excluir.html'
    success_url = reverse_lazy('listar-celulas')

class CelulasList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = ["Administradores", "Secretaria", "Pastor", "Líderes", "Celulas"]
    model = Celulas
    template_name = 'celulas/listas/celulas-list.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Você precisa estar autenticado para acessar este módulo.")

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if not hasattr(request.user, 'perfil'):
            raise PermissionDenied("Seu perfil não está configurado corretamente.")

        if not request.user.perfil.acesso_celulas:
            raise PermissionDenied("Você não tem permissão para acessar este módulo.")

        return super().dispatch(request, *args, **kwargs)
    

class CelulasView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = "Administradores", u"Lideres", u"Secretaria", u"Pastor"
    template_name = 'celulas/visualizar.html'
    model = Celulas
    context_object_name = 'celulas'

class GerarPDFCelulas(GroupRequiredMixin, LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Lideres", u"Secretaria", u"Pastor"

    def get(self, request, *args, **kwargs):
        # Dados para o PDF
        celulas = Celulas.objects.all()
        data = {
            'celulas': celulas,
            'data_atual': datetime.now().strftime("%d/%m/%Y"),
            'page_num': 1
        }
        
        # Gerar PDF
        pdf = render_to_pdf('celulas/pdf_template.html', data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "celulas_%s.pdf" % datetime.now().strftime("%Y%m%d_%H%M%S")
            content = "inline; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Erro ao gerar PDF")