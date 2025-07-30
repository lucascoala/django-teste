from django.http import JsonResponse
from django.db.models import Q
from membros.models import Membros

def buscar_alunos(request):
    """
    Função para buscar alunos via AJAX.
    Retorna uma lista de alunos filtrados pelo termo de busca.
    """
    termo_busca = request.GET.get('search', '')
    
    if not termo_busca:
        return JsonResponse({'results': []})
    
    # Filtra membros ativos que correspondem ao termo de busca
    alunos = Membros.objects.filter(
        (Q(cargo=Membros.MEMBRO_ATIVO) | 
         Q(cargo=Membros.PRESBITERO) | 
         Q(cargo=Membros.DIACONO)) & 
        (Q(nome__icontains=termo_busca) | 
         Q(email__icontains=termo_busca))
    ).order_by('nome')
    
    # Formata os resultados para JSON no formato esperado pelo Select2
    resultados = [{
        'id': aluno.id,
        'text': f"{aluno.nome} ({getattr(aluno, 'email', '')})"
    } for aluno in alunos[:20]]  # Limita a 20 resultados para performance
    
    return JsonResponse({'results': resultados})