from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView
from .models import ReuniaoConselho, ReuniaoDiaconos
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

class ReuniaoConselhoCreate(GroupRequiredMixin,LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Presbíteros", u"Presbíteros", u"Pastor"
    model = ReuniaoConselho
    fields = ['data', 'pauta', 'relatorio', 'local', 'presbiteros']
    template_name = 'reunioes/form.html'
    success_url = reverse_lazy('listar-reuniaoconselho')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastrar reunião do conselho"
        context['botao'] = "Cadastrar"
        
        return context

class ReuniaoConselhoUpdade(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Presbíteros"
    model = ReuniaoConselho
    fields = ['data', 'pauta', 'relatorio', 'local', 'presbiteros']
    template_name = 'reunioes/form.html'
    success_url = reverse_lazy('listar-reuniaoconselho')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Editar reunião do conselho"
        context['botao'] = "Salvar"
        
        return context

class ReuniaoConselhoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Presbíteros"
    model = ReuniaoConselho
    template_name = 'reunioes/form-excluir.html'
    success_url = reverse_lazy('listar-reuniaoconselho')
    

class ReuniaoConselhoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = ["Administradores", "Secretaria", "Pastor", "Presbitero"]  # Defina os grupos necessários
    model = ReuniaoConselho  # Ou o modelo correto
    template_name = 'reunioes/listas/reuniaoconselho-list.html'
    paginate_by = 10

    def get_queryset(self):
        # Aqui você pode definir a lógica do queryset, se necessário
        return super().get_queryset()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if not request.user.perfil.acesso_reuniao:
            raise PermissionDenied("Você não tem permissão para acessar este módulo.")
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tiporeuniao'] = "reunião do conselho"
        
        return context

    def get_queryset(self):
        txt_nome = self.request.GET.get('data')
        if txt_nome:
            reuniaoconselho = ReuniaoConselho.objects.filter(data__icontains=txt_nome)
        else:
            reuniaoconselho = ReuniaoConselho.objects.all()
        return reuniaoconselho

class ReuniaoConselhoView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Presbíteros"
    template_name = 'reunioes/visualizar-conselho.html'
    model = ReuniaoConselho
    context_object_name = 'reuniaoconselho'
    

#_____________________________________________________________________________________


class ReuniaoDiaconosCreate(GroupRequiredMixin,LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Diaconos"
    model = ReuniaoDiaconos
    fields = ['data', 'pauta', 'relatorio', 'local', 'diaconos']
    template_name = 'reunioes/form-diaconos.html'
    success_url = reverse_lazy('listar-reuniaodiaconos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastrar reunião dos diaconos"
        context['botao'] = "Cadastrar"
        
        return context

class ReuniaoDiaconosUpdade(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Diaconos"
    model = ReuniaoDiaconos
    fields = ['data', 'pauta', 'relatorio', 'local', 'diaconos']
    template_name = 'reunioes/form-diaconos.html'
    success_url = reverse_lazy('listar-reuniaodiaconos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Editar reunião dos diaconos"
        context['botao'] = "Salvar"
        
        return context

class ReuniaoDiaconosDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Diaconos"
    model = ReuniaoDiaconos
    template_name = 'reunioes/form-excluir-diaconos.html'
    success_url = reverse_lazy('listar-reuniaodiaconos')
    

class ReuniaoDiaconosList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Diaconos"
    model = ReuniaoDiaconos
    template_name = 'reunioes/listas/reuniaodiaconos-list.html'
    paginate_by = 5

    def get_queryset(self):
        txt_nome = self.request.GET.get('data')
        if txt_nome:
            reuniaodiaconos = ReuniaoDiaconos.objects.filter(data__icontains=txt_nome)
        else:
            reuniaodiaconos = ReuniaoDiaconos.objects.all()
        return reuniaodiaconos

class ReuniaoDiaconosView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Diaconos"
    template_name = 'reunioes/visualizar-diaconos.html'
    model = ReuniaoDiaconos
    context_object_name = 'reuniaodiaconos'