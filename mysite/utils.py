try:
    from xhtml2pdf import pisa
except ImportError:
    raise ImportError(
        "Biblioteca xhtml2pdf não encontrada. "
        "Por favor, instale usando: pip install xhtml2pdf"
    )

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    
    # Adiciona o caminho para os arquivos estáticos (imagens, css, etc)
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")), 
        result,
        encoding='utf-8',
        link_callback=fetch_resources
    )
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def fetch_resources(uri, rel):
    """
    Callback para carregar imagens e outros recursos no PDF
    """
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    elif uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    else:
        path = uri

    return path 