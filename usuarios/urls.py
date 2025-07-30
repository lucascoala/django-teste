from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UsuarioCreate, UsuarioUpdate, AlterarSenhaView, GerarPDFUsuarios, UsuarioDelete, UsuarioList

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html',
        redirect_authenticated_user=True,
        success_url='/'
    ), name='login'),
   
   path('logout/', auth_views.LogoutView.as_view(),name='logout'),
   path('registrar/', UsuarioCreate.as_view(), name='registrar'),
   path('atualizar-dados/', UsuarioUpdate.as_view(),name='atualizar-dados'),
   path('alterar-senha/', AlterarSenhaView.as_view(), name='alterar-senha'),
   path('gerar-pdf/', GerarPDFUsuarios.as_view(), name='gerar-pdf-usuarios'),
   path('deletar/<int:pk>/', UsuarioDelete.as_view(), name='deletar-usuario'),
   path('listar/', UsuarioList.as_view(), name='listar-usuarios'),
   # Removed duplicate registration path that was using RegisterView
]
