from django.http import HttpResponse
from django.template.loader import render_to_string
#from weasyprint import HTML

from financemanager.models import Payment


def payments_report(request):
    """Generate pdf."""
    # Model data
    data = {'object_list': Payment.objects.filter(financemanager=request.User.financemanager)}
    # Rendered
    html_string = render_to_string('financemanager/reports/payments-pdf.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = "inline; filename=airport-payments.pdf "
    return response
