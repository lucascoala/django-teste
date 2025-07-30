from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from .models import Missao

class MissaoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"secretaria", u"Pastor", u"Tesoureiro"
    model = Missao
    fields = ['nome_missionario', 'local', 'valor_aplicado']
    template_name = 'missao/form.html'
    success_url = reverse_lazy('listar-missoes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastrar Missão"
        context['botao'] = "Cadastrar"
        return context

class MissaoList(LoginRequiredMixin, ListView):  # Removido GroupRequiredMixin
    login_url = reverse_lazy('login')
    context_object_name = 'missoes'
    model = Missao
    template_name = 'missao/missao-list.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
            
        # Verifica se o usuário tem perfil e se tem acesso ao módulo
        if not hasattr(request.user, 'perfil') or not request.user.perfil.acesso_missao:
            raise PermissionDenied("Você não tem permissão para acessar este módulo.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        local = self.request.GET.get('local')

        if local:
            queryset = queryset.filter(local__icontains=local)

        return queryset.order_by('-nome_missionario')

class MissaoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"secretaria", u"Pastor"
    model = Missao
    fields = ['nome_missionario', 'local', 'valor_aplicado']
    template_name = 'missao/form.html'
    success_url = reverse_lazy('listar-missoes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Editar Missão"
        context['botao'] = "Salvar"
        return context

class MissaoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Pastor", u"Scretaria"
    model = Missao
    template_name = 'missao/form-excluir.html'
    success_url = reverse_lazy('listar-missoes')

class MissaoView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"secretaria", u"Pastor"
    model = Missao
    template_name = 'missao/missao-view.html'