from io import BytesIO

from django.template.loader import get_template
from xhtml2pdf import pisa


def generate_pdf(template_name, context):
    template = get_template(template_name)
    html = template.render(context)

    result = BytesIO()

    pdf = pisa.CreatePDF(
        html,
        dest=result
    )

    if pdf.err:
        return None

    return result.getvalue()