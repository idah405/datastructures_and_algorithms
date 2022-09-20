from datetime import datetime
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, ListView
from flights.models import service, ClientService, Appointment
from financemanager.forms import PaymentForm
from financemanager.models import Payment, financemanager
from client.forms import clientForm, clientProfileForm, clientSignUpForm, clientAuthenticationForm, \
    clientFeedbackForm
from client.models import client
from Users.decorators import client_required
from Users.models import User
from Users.tokens import account_activation_token
from utils.utils import generate_key
import django.utils.timezone


class clientLoginView(LoginView):
    template_name = 'accounts.html'
    authentication_form = clientAuthenticationForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        print(form.get_user())
        login(self.request, form.get_user())
        data = {'message': 'User has logged in successfully'}
        return JsonResponse(data)

    def form_invalid(self, form):
        print(form)
        messages.error(self.request, form.non_field_errors)
        return JsonResponse({'form': form.errors}, safe=False)


class clientSignUpView(CreateView):
    form_class = clientSignUpForm
    template_name = 'client/include/accounts.html'

    def get_form_kwargs(self):
        kwargs = super(clientSignUpView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors)

    def form_valid(self, form):
        name = form.instance.first_name
        last = form.instance.last_name
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        current_site = get_current_site(self.request)
        to_email = form.cleaned_data.get('email')
        subject = f'client Email Verification.'
        msg_plain = render_to_string('client/emails/email.txt', {'user_name': user.get_full_name, })
        msg_html = render_to_string('client/emails/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(subject, msg_plain, 'Handyman 254', [to_email], html_message=msg_html)
        data = {"message": f"Hi {name} {last}, your account has been created successfully verify your email."}
        return JsonResponse(data)


class VerifyEmail(View):

    def get(self, *args, **kwargs):
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = client.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            if user.is_verified:
                messages.info(self.request, "you've already confirmed your email.")
            elif not user.is_verified:
                user.is_verified = True
                user.save()
                messages.info(self.request, "You've successfully verified your email. use your email to login")
            return redirect('client:login')
        else:
            data = {'message': 'The confirmation link was invalid, possibly because it has already been used.'}
            return JsonResponse(data)


#class IndexView(View):
    #template_name = "client/index.html"
    #def appointment(request):

    #def get(self, *args, **kwargs):
        #ClientService = ClientService.objects.filter(Day__gte=datetime())
       # ClientService = ClientService.objects.filter(Day__gte=datetime.now())
        #return render(self.request, self.template_name)
class IndexView(View):
    template_name = "client/index.html"

    def get(self, *args, **kwargs):
        global service
        global ClientService

        services = service.objects.all()
        ClientServices = ClientService.objects.filter(Day__gte=timezone.now())
        return render(self.request, self.template_name, { 'services': services,'ClientServices': ClientServices})

class AboutView(View):
    template_name = 'client/about-us.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class ContactView(View):
    template_name = "client/contact.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class FeedbackView(CreateView):
    form_class = clientFeedbackForm
    template_name = "client/feedback.html"

    def get_form_kwargs(self):
        kwargs = super(FeedbackView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.admin = User.objects.filter(is_handyman=True).first()
        instance.user = self.request.user.client
        instance.save()
        messages.success(self.request, 'Thank you for your feedback.')
        return redirect('client:index')


@method_decorator(client_required, name='dispatch')
class ProfileView(View):
    template_name = "client/profile.html"

    def get(self, *args, **kwargs):
        request = self.request
        p_form = clientProfileForm(instance=request.user.client.clientprofile)
        form = clientForm(instance=request.user.client)
        return render(self.request, self.template_name, {'p_form': p_form, 'form': form, })

    def post(self, *args, **kwargs):
        request = self.request
        p_form = clientProfileForm(request.POST, request.FILES, instance=request.user.client.clientprofile)
        form = clientForm(request.POST, instance=request.user.client)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, "Your Profile has been updated!")
        return render(self.request, self.template_name, {'p_form': p_form, 'form': form, })


class ClientServiceListView(ListView):
    template_name = "client/ClientService.html"
    paginate_by = 5

    def get_queryset(self):
        object_list = ClientService.objects.filter(Day__gte=datetime.now())
        return object_list

    def post(self, *args, **kwargs):
        service = self.request.POST.get('ClientService')
        object_list = self.get_queryset().filter(service=service)
        return render(self.request, self.template_name, {'object_list': object_list})


@client_required
def Appointment_api(request):
    if request.method == "POST":
     ClientService_id = request.POST.get('Appointment_id')
    if ClientService.objects.filter(id=ClientService_id).exists():
            ClientService = ClientService.objects.get(id=ClientService_id)
            # making sure only available seats are booked
            if Appointment.objects.filter(ClientService=ClientService).count() < ClientService.seats_no:
                if Appointment.objects.filter(ClientService=ClientService, client=request.user.client).exists():
                    messages.info(request, "Appointment has already been made")
                else:
                    Appointment.objects.create(ClientService=ClientService, client=request.user.client, code=generate_key(12, 12))
                    messages.success(request, "Appointment has been booked successfully")
            else:
                messages.info(request, "Sorry all Handymen are booked")
            return redirect('client:Appointment')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@client_required
def appointment(request):
    Appointments = Appointment.objects.filter(client=request.user.client, ClientService__Day=datetime.now(),
                                      paid=False).order_by('-created')
    paid_Appointments = Appointment.objects.filter(client=request.user.client, paid=True).order_by('-created')
    return render(request, 'client/Appointment.html', {'Appointments': Appointments, 'paid_Appointments': paid_Appointments})


@client_required
def cancel_Appointment(request, slug):
    Appointment_obj = get_object_or_404(Appointment, slug=slug)
    Appointment_obj.delete()
    messages.info(request, "Apointment has been cancelled.")
    return redirect(reverse("client:index"))


@client_required
def Appointment_payment(request, slug):
    Appointment_obj = get_object_or_404(Appointment, slug=slug)
    form = PaymentForm()
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.code = generate_key(11, 11)
            instance.client = Appointment_obj
            instance.client = request.user.client
            instance.amount = Appointment_obj.clientService.price
            instance.financemanager = financemanager.objects.filter(is_archived=False, is_active=True).first()
            if Payment.objects.filter(client=instance.client, Appointment=instance.Appointment).exists():
                messages.info(request, 'payment has already been made')
            elif Payment.objects.filter(mpesa=instance.mpesa).exists():
                messages.info(request, "Mpesa code has already been used")
            else:
                instance.save()
                Appointment_obj.paid = True
                Appointment_obj.save()
                messages.success(request, 'Payment has been done successfully')
                return redirect(reverse('client:success_page', kwargs={'slug': Appointment_obj.slug}))
    return render(request, 'client/payment.html', {'form': form, 'Appointment_obj': Appointment_obj})


@client_required
def change_password(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
    return render(request, 'client/change-password.html', {'form': form})


@client_required
def success_page(request, slug):
    Appointment_obj = get_object_or_404(Appointment, slug=slug)
    return render(request, 'client/success-page.html', {'Apontment_obj': Appointment_obj})


def faq(request):
    return render(request, 'client/faqs.html')


@client_required
def receipts(request):
    tickets = Appointment.objects.filter(client=request.user.client, paid=True)
    return render(request, 'client/receipts.html', {'tickets': tickets})


def log_out(request):
    logout(request)
    messages.info(request, f"You've logged out successfully.")
    return redirect('client:index')
