from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from .models import Visitantes
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class VisitantesCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria", u"Pastor", u"Diacono", u"Presbitero"
    model = Visitantes
    fields = ['nome', 'data', 'endereco', 'telefone', 'filhos']
    template_name = 'visitantes/form.html'
    success_url = reverse_lazy('listar-visitantes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastro de visitantes"
        context['botao'] = "Cadastrar"
        
        return context

class VisitantesUpdade(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria"
    model = Visitantes
    fields = ['nome', 'data', 'endereco', 'telefone', 'filhos']
    template_name = 'visitantes/form.html'
    success_url = reverse_lazy('listar-visitantes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Editar celula"
        context['botao'] = "Salvar"
        
        return context

class VisitantesDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria"
    model = Visitantes
    template_name = 'visitantes/form-excluir.html'
    success_url = reverse_lazy('listar-visitantes')

class VisitantesList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria", u"Pastor", u"Diacono", u"Presbitero"
    model = Visitantes
    template_name = 'visitantes/listas/visitantes-list.html'
    paginate_by = 5


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Você precisa estar autenticado para acessar este módulo.")

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if not hasattr(request.user, 'perfil'):
            raise PermissionDenied("Seu perfil não está configurado corretamente.")

        if not request.user.perfil.acesso_visitantes:
            raise PermissionDenied("Você não tem permissão para acessar este módulo.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        txt_nome = self.request.GET.get('nome')
        if txt_nome:
            visitantes = Visitantes.objects.filter(nome__icontains=txt_nome)
        else:
            visitantes = Visitantes.objects.all()
        return visitantes

class VisitantesView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria"
    template_name = 'visitantes/visualizar.html'
    model = Visitantes
    context_object_name = 'visitantes'

