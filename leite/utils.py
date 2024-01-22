from unittest import result
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime

def gerar_relatorio(template_src,context_dict=dict()):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    return HttpResponse(result.getvalue(),content_type="application/pdf")


def formataData(data):
    date = datetime.strptime(data, '%d/%m/%Y')
    return datetime.strftime(date, '%Y-%m-%d')