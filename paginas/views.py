from django.views.generic import TemplateView, FormView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View


class IndexView(TemplateView):
    template_name = "paginas/index.html"


class SobreView(TemplateView):
    template_name = "paginas/sobre.html"


class PoliticaPrivacidadeView(TemplateView):
    template_name = "paginas/politica_privacidade.html"


class TermosUsoView(TemplateView):
    template_name = "paginas/termos_uso.html"


class ConsentimentoView(TemplateView):
    template_name = "paginas/consentimento.html"


class SalvarConsentimentoView(View):
    def post(self, request, *args, **kwargs):
        # Aqui seria implementada a lógica para salvar o consentimento no banco de dados
        # Por exemplo, criar um modelo de Consentimento e salvar os dados do formulário
        
        # Exemplo simplificado:
        nome = request.POST.get('nome')
        finalidades = request.POST.getlist('finalidades[]')
        categorias = request.POST.getlist('categorias[]')
        
        # Aqui você salvaria essas informações no banco de dados
        # consentimento = Consentimento.objects.create(usuario=request.user, ...)
        
        messages.success(request, 'Seu consentimento foi registrado com sucesso!')
        return HttpResponseRedirect(reverse_lazy('index'))
