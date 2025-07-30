from django.contrib import admin
from .models import Despesas

@admin.register(Despesas)
class DespesasAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'valor', 'data_vencimento', 'clc', 'status']
    list_filter = ['status', 'clc', 'tipo', 'forma_pagamento']
    search_fields = ['descricao', 'clc']
    date_hierarchy = 'data_vencimento'
    list_per_page = 20
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('descricao', 'valor', 'data_vencimento', 'tipo', 'categoria')
        }),
        ('Pagamento', {
            'fields': ('forma_pagamento', 'status', 'data_pagamento', 'comprovante')
        }),
        ('Informações Adicionais', {
            'fields': ('observacao', 'usuario_cadastro'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['usuario_cadastro', 'data_cadastro', 'ultima_alteracao']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é uma nova despesa
            obj.usuario_cadastro = request.user
        super().save_model(request, obj, form, change)
