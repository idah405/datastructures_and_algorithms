from django.http import HttpResponse
from django.template.loader import render_to_string
#from weasyprint import HTML

from flights.models import Appointment, ClientService


def Appointment_report(request):
    """Generate pdf."""
    # Model data
    data = {'object_list': Appointment.objects.filter(ClientService__Service=request.User.handyman.handymanprofile.Service)}
    # Rendered
    html_string = render_to_string('handyman/reports/Appointment-pdf.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = "inline; filename=ClientService-Appointments.pdf "
    return response


def ClientService_report(request):
    """Generate pdf."""
    # Model data
    data = {'object_list': ClientService.objects.filter(Service=request.User.handyman.handymanprofile.Service)}
    # Rendered
    html_string = render_to_string('handyman/reports/flights-pdf.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = "inline; filename=airport-flights.pdf "
    return response
