from django.contrib import admin
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Perfil

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False

class CustomUserAdmin(admin.ModelAdmin):
    inlines = (PerfilInline,)
    list_display = ('username', 'email', 'is_active', 'is_staff')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Garante que o perfil existe
        perfil, created = Perfil.objects.get_or_create(usuario=obj)
        
        # Se é um superusuário, ativa todos os acessos
        if obj.is_superuser:
            perfil.acesso_usuarios = True
            perfil.acesso_celulas = True
            perfil.acesso_visitantes = True
            perfil.acesso_membros = True
            perfil.acesso_financeiro = True
            perfil.acesso_salas = True
            perfil.acesso_reunioes = True
            perfil.acesso_matriz = True
            perfil.acesso_missao = True
            perfil.acesso_despesas = True
            perfil.acesso_contribuicoes = True
            perfil.save()

            # Adiciona todas as permissões do sistema
            all_permissions = Permission.objects.all()
            for perm in all_permissions:
                obj.user_permissions.add(perm)
        elif not change:  # Se é um novo usuário não superusuário
            # Ativa o acesso ao módulo de usuários por padrão
            perfil.acesso_usuarios = True
            perfil.save()

            # Adiciona permissões do módulo de usuários
            content_type = ContentType.objects.get_for_model(User)
            permissions = Permission.objects.filter(content_type=content_type)
            for perm in permissions:
                obj.user_permissions.add(perm)
        
        obj.save()

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
