from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic import View, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.core.exceptions import PermissionDenied, ValidationError
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from datetime import datetime
import logging
from usuarios.models import Perfil
from .forms import UsuarioForm
from mysite.utils import render_to_pdf

logger = logging.getLogger(__name__)

class UsuarioCreate(CreateView):
    template_name = "usuarios/form.html"
    form_class = UsuarioForm
    success_url = reverse_lazy('listar-usuarios')

    def form_valid(self, form):
        try:
            logger.debug("Iniciando validação do formulário")
            logger.debug(f"Dados do formulário: {form.cleaned_data}")
            
            with transaction.atomic():
                # Salvando o usuário
                user = form.save(commit=False)
                user.is_active = True
                user.is_staff = True
                user.set_password(form.cleaned_data['password1'])
                user.save()

                logger.debug(f"Usuário criado: {user.username}")

                # Associa o grupo (se houver)
                grupo = form.cleaned_data.get('grupo')
                if grupo:
                    user.groups.clear()
                    user.groups.add(grupo)
                    logger.debug(f"Grupo adicionado: {grupo}")

                # Garantindo que o perfil seja criado ou atualizado corretamente
                perfil, created = Perfil.objects.get_or_create(
                    usuario=user,
                    defaults={
                        'acesso_celulas': form.cleaned_data.get('acesso_celulas', True),
                        'acesso_visitantes': form.cleaned_data.get('acesso_visitantes', True),
                        'acesso_membros': form.cleaned_data.get('acesso_membros', True),
                        'acesso_financeiro': form.cleaned_data.get('acesso_financeiro', True),
                        'acesso_salas': form.cleaned_data.get('acesso_salas', True),
                        'acesso_reunioes': form.cleaned_data.get('acesso_reunioes', True),
                        'acesso_matriz': form.cleaned_data.get('acesso_matriz', True),
                        'acesso_missao': form.cleaned_data.get('acesso_missao', True),
                        'acesso_usuarios': form.cleaned_data.get('acesso_usuarios', True),
                        'acesso_despesas': form.cleaned_data.get('acesso_despesas', True),
                        'acesso_contribuicoes': form.cleaned_data.get('acesso_contribuicoes', True)
                    }
                )

                # Se o perfil já existia, atualize as permissões
                if not created:
                    perfil.acesso_celulas = form.cleaned_data.get('acesso_celulas', perfil.acesso_celulas)
                    perfil.acesso_visitantes = form.cleaned_data.get('acesso_visitantes', perfil.acesso_visitantes)
                    perfil.acesso_membros = form.cleaned_data.get('acesso_membros', perfil.acesso_membros)
                    perfil.acesso_financeiro = form.cleaned_data.get('acesso_financeiro', perfil.acesso_financeiro)
                    perfil.acesso_salas = form.cleaned_data.get('acesso_salas', perfil.acesso_salas)
                    perfil.acesso_reunioes = form.cleaned_data.get('acesso_reunioes', perfil.acesso_reunioes)
                    perfil.acesso_matriz = form.cleaned_data.get('acesso_matriz', perfil.acesso_matriz)
                    perfil.acesso_missao = form.cleaned_data.get('acesso_missao', perfil.acesso_missao)
                    perfil.acesso_usuarios = form.cleaned_data.get('acesso_usuarios', perfil.acesso_usuarios)
                    perfil.acesso_despesas = form.cleaned_data.get('acesso_despesas', perfil.acesso_despesas)
                    perfil.acesso_contribuicoes = form.cleaned_data.get('acesso_contribuicoes', perfil.acesso_contribuicoes)
                    perfil.save()

                logger.debug(f"Perfil criado/atualizado: {perfil.id}")

                messages.success(self.request, f'Usuário {user.username} cadastrado com sucesso!')
                return redirect(self.success_url)
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {str(e)}")
            messages.error(self.request, f'Erro ao cadastrar usuário: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.error(f"Erros no formulário: {form.errors}")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Erro no campo {field}: {error}')
        return super().form_invalid(form)

class UsuarioUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = ("Administradores", "Secretaria", "Pastor")
    template_name = "usuarios/form.html"
    model = User
    form_class = UsuarioForm
    success_url = reverse_lazy('listar-usuarios')

    def form_valid(self, form):
        user = form.save()
        grupo = form.cleaned_data.get('grupo')
        
        user.groups.clear()
        if grupo:
            user.groups.add(grupo)

        perfil, created = Perfil.objects.get_or_create(usuario=user)
        # Atualizando as permissões no perfil
        perfil.acesso_celulas = form.cleaned_data.get('acesso_celulas', perfil.acesso_celulas)
        perfil.acesso_visitantes = form.cleaned_data.get('acesso_visitantes', perfil.acesso_visitantes)
        perfil.acesso_membros = form.cleaned_data.get('acesso_membros', perfil.acesso_membros)
        perfil.acesso_financeiro = form.cleaned_data.get('acesso_financeiro', perfil.acesso_financeiro)
        perfil.acesso_salas = form.cleaned_data.get('acesso_salas', perfil.acesso_salas)
        perfil.acesso_reunioes = form.cleaned_data.get('acesso_reunioes', perfil.acesso_reunioes)
        perfil.acesso_matriz = form.cleaned_data.get('acesso_matriz', perfil.acesso_matriz)
        perfil.acesso_missao = form.cleaned_data.get('acesso_missao', perfil.acesso_missao)
        perfil.acesso_usuarios = form.cleaned_data.get('acesso_usuarios', perfil.acesso_usuarios)
        perfil.acesso_despesas = form.cleaned_data.get('acesso_despesas', perfil.acesso_despesas)
        perfil.acesso_contribuicoes = form.cleaned_data.get('acesso_contribuicoes', perfil.acesso_contribuicoes)
        perfil.save()

        messages.success(self.request, f'Usuário {user.username} atualizado com sucesso!')
        return super().form_valid(form)


class AlterarSenhaView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'usuarios/alterar_senha.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, 'Sua senha foi alterada com sucesso!')
        return super().form_valid(form)

class GerarPDFUsuarios(GroupRequiredMixin, LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    group_required = "Administradores"

    def get(self, request, *args, **kwargs):
        try:
            perfis = Perfil.objects.select_related('usuario').all()
            data = {
                'perfis': perfis,
                'data_atual': datetime.now().strftime("%d/%m/%Y"),
            }
            pdf = render_to_pdf('usuarios/pdf_template.html', data)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = f"inline; filename='usuarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf'"
                return response
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            messages.error(request, 'Erro ao gerar PDF.')
        return HttpResponse("Erro ao gerar PDF")

class UsuarioList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = ("Administradores", "Secretaria", "Pastor")
    model = User
    template_name = 'usuarios/listar_usuarios.html'
    context_object_name = 'usuarios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UsuarioForm()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.perfil.acesso_usuarios:
            raise PermissionDenied("Você não tem permissão para acessar este módulo.")
        return super().dispatch(request, *args, **kwargs)

class UsuarioDelete(GroupRequiredMixin, LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    group_required = "Administradores"

    def post(self, request, pk):
        usuario = get_object_or_404(User, pk=pk)
        if usuario == request.user:
            messages.error(request, 'Você não pode deletar seu próprio usuário.')
            return redirect('listar-usuarios')
        usuario.delete()
        messages.success(request, f'Usuário {usuario.username} deletado com sucesso!')
        return redirect('listar-usuarios')
