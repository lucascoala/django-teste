from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from .models import Salas  # Importar o modelo Salas do módulo correto
from .forms import SalasForm
from django.db.models import Q
from mysite.utils import render_to_pdf
from django.views.generic import View
from django.http import HttpResponse
from datetime import datetime

class SalasCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Professor", u"Secretaria", u"Pastor", u"Tesoureiro"
    model = Salas
    form_class = SalasForm
    template_name = 'salas/sala_form.html'
    success_url = reverse_lazy('listar-salas')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Você precisa estar autenticado para acessar este módulo.")

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if not hasattr(request.user, 'perfil'):
            raise PermissionDenied("Seu perfil não está configurado corretamente.")

        if not request.user.perfil.acesso_salas:
            raise PermissionDenied("Você não tem permissão para acessar este módulo.")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastrar Sala"
        context['botao'] = "Cadastrar"
        from membros.models import Membros
        context['alunos'] = Membros.objects.filter(cargo=Membros.MEMBRO_ATIVO).order_by('nome')
        return context

    def form_valid(self, form):
        sala = form.save()
        
        # Processa as presenças dos alunos
        alunos_ids = self.request.POST.getlist('alunos[]')
        for aluno_id in alunos_ids:
            presente = bool(self.request.POST.get(f'presenca_{aluno_id}'))
            sala.presenca_set.create(aluno_id=aluno_id, presente=presente)
        
        return super().form_valid(form)
        
        # Processar presenças
        for key, value in self.request.POST.items():
            if key.startswith('presenca_'):
                membro_id = int(key.split('_')[1])
                from membros.models import Membros
                membro = Membros.objects.get(id=membro_id)
                sala.presenca_set.create(aluno=membro, presente=True)
        
        return response

class SalasList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Professores", u"Secretaria", u"Pastor", u"Professor"
    model = Salas
    template_name = 'salas/listas/salas-list.html'
    paginate_by = 10
    model = Salas
    template_name = 'salas/listas/salas-list.html'
    paginate_by = 10
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Você precisa estar autenticado para acessar este módulo.")

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if not hasattr(request.user, 'perfil'):
            raise PermissionDenied("Seu perfil não está configurado corretamente.")

        if not request.user.perfil.acesso_salas:
            raise PermissionDenied("Você não tem permissão para acessar este módulo.")

        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Professores').exists():
            # Professores só veem suas próprias salas
            queryset = queryset.filter(professor=self.request.user)
        return queryset.order_by('-data')
        data = self.request.GET.get('data')
        
        if data:
            queryset = queryset.filter(data=data)
        
        return queryset.order_by('-data')

class SalasUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Professores", u"Secretaria", u"Pastor", u"Tesoureiro"
    model = Salas
    form_class = SalasForm
    template_name = 'salas/form.html'
    success_url = reverse_lazy('listar-salas')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Editar Sala"
        context['botao'] = "Salvar"
        return context

class SalasDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administrador", u"Professores", u"Secretaria", u"Pastor"
    model = Salas
    template_name = 'salas/form-excluir.html'
    success_url = reverse_lazy('listar-salas')

class SalasView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Professor", u"Secretaria", u"Pastor"
    model = Salas
    template_name = 'salas/listas/salas-view.html'

class GerarPDFSalas(GroupRequiredMixin, LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    group_required = u"Administradores", u"Professor", u"Secretaria", u"Pastor"
    model = Salas

    def get(self, request, *args, **kwargs):
        # Dados para o PDF
        salas = Salas.objects.all()
        context_data = {
            'salas': salas,
            'data_atual': datetime.now().strftime("%d/%m/%Y"),
            'page_num': 1
        }
        
        # Gerar PDF
        pdf = render_to_pdf('salas/pdf_template.html', context_data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "salas_%s.pdf" % datetime.now().strftime("%Y%m%d_%H%M%S")
            content = "inline; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Erro ao gerar PDF")