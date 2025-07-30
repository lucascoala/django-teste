from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView
from .models import MatrizGUT, Matriz5W2H
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

class MatrizGUTCreate(GroupRequiredMixin,LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria", u"Pastor"
    model = MatrizGUT
    fields = ['nome', 'causa', 'grupo', 'gravidade', 'urgencia', 'tendencia']
    template_name = 'matrizGUT/form.html'
    success_url = reverse_lazy('listar-matrizGUT')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tipomatriz'] = "Cadastrar MatrizGUT"
        context['botao'] = "Cadastrar"
        
        return context

class MatrizGUTUpdade(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria"
    model = MatrizGUT
    fields = ['nome', 'causa', 'grupo', 'gravidade', 'urgencia', 'tendencia']
    template_name = 'matrizGUT/form.html'
    success_url = reverse_lazy('listar-matrizGUT')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tipomatriz'] = "MatrizGUT"
        context['botao'] = "Salvar"
        
        return context

class MatrizGUTDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria"
    model = MatrizGUT
    template_name = 'matrizGUT/form-excluir.html'
    success_url = reverse_lazy('listar-matrizGUT')
    

class MatrizGUTList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria"
    model = MatrizGUT
    template_name = 'matrizGUT/listas/matrizGUT-list.html'
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if not request.user.perfil.acesso_matriz:
            raise PermissionDenied("Você não tem permissão para acessar este módulo.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tipomatriz'] = "MatrizGUT"
        
        return context

    def get_queryset(self):
        txt_nome = self.request.GET.get('nome')
        if txt_nome:
            matrizGUT = MatrizGUT.objects.filter(nome__icontains=txt_nome)
        else:
            matrizGUT = MatrizGUT.objects.all()
        return matrizGUT

class MatrizGUTView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria"
    template_name = 'matrizGUT/visualizar-matrizGUT.html'
    model = MatrizGUT
    context_object_name = 'matrizGUT'


#-----------------------------------------------------------------------------------------------------------

class Matriz5W2HCreate(GroupRequiredMixin,LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria"
    model = Matriz5W2H
    fields = ['what', 'why', 'who', 'when', 'where', 'how', "how_much"]
    template_name = 'matrizGUT/form.html'
    success_url = reverse_lazy('listar-matriz5W2H')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tipomatriz'] = "Cadastrar Matriz5W2H"
        context['botao'] = "Cadastrar"
        
        return context

class Matriz5W2HUpdade(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria"
    model = Matriz5W2H
    fields = ['what', 'why', 'who', 'when', 'where', 'how', "how_much"]
    template_name = 'matrizGUT/form.html'
    success_url = reverse_lazy('listar-matriz5W2H')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tipomatriz'] = "Matriz5W2H"
        context['botao'] = "Salvar"
        
        return context

class Matriz5W2HDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria"
    model = Matriz5W2H
    template_name = 'matrizGUT/form-excluir.html'
    success_url = reverse_lazy('listar-Matriz5W2H')
    

class Matriz5W2HList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria"
    model = Matriz5W2H
    template_name = 'matrizGUT/listas/matriz5W2H-list.html'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tipomatriz'] = "Matriz5W2H"
        
        return context

    def get_queryset(self):
        txt_nome = self.request.GET.get('what')
        if txt_nome:
            matriz5W2H = Matriz5W2H.objects.filter(what__icontains=txt_nome)
        else:
            matriz5W2H = Matriz5W2H.objects.all()
        return matriz5W2H

class Matriz5W2HView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Secretaria"
    template_name = 'matrizGUT/visualizar.html'
    model = Matriz5W2H
    context_object_name = 'matriz5W2H'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tipomatriz'] = "Matriz5W2H"
        
        return context