from decimal import Context
from difflib import context_diff
from multiprocessing import context
from django.shortcuts import render

# Create your views here.

#def index(request):
    #return render(request, "index.html")
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView

from flights.models import Appointment, ClientService
from handyman.forms import handymanAuthenticationForm, handymanSignUpForm, handymanProfileForm, \
    handymanForm, handymanFeedbackForm
from handyman.models import handymanFeedback, handyman, CheckAppointments


class handymanLoginView(LoginView):
    template_name = "handyman/login.html"
    authentication_form = handymanAuthenticationForm

    def form_valid(self, form):
        User = form.get_user()
        if User is not None:
            login(self.request, User)
            messages.success(self.request, f"Hi {User.get_full_name}, you've logged in successfully.")
        return redirect('handyman:index')


class handymanSignUpView(CreateView):
    form_class = handymanSignUpForm
    template_name = "handyman/register.html"

    def form_valid(self, form):
        User = form.save(commit=False)
        User.save()
        messages.success(self.request, f"Hi {User.get_full_name}, your account has been created successfully wait for "
                                       f"approval.")
        return redirect('handyman:login')


class IndexView(View):
    template_name = "handyman/index.html"

    def get(self, *args, **kwargs):
        context = {}
        request = self.request
        context['Appointments_count'] = Appointment.objects.filter(service=request.user.handyman.handymanprofile.service).count()
        context['ClientService_count'] = ClientService.objects.filter(service=request.user.handyman.handymanprofile.service).count()  
        context['attendants_count'] = handyman.objects.filter(
            User_type="Electrician", handymanprofile__service=request.user.handyman.handymanprofile.service).count()        
        return render(self.request, self.template_name, context)


class ProfileView(View):
    template_name = "handyman/profile.html"

    def get(self, *args, **kwargs):
        request = self.request
        p_form = handymanProfileForm(instance=request.user.handyman.handymanprofile)
        form = handymanForm(instance=request.user.handyman)
        return render(self.request, self.template_name, {"p_form": p_form, "form": form})

    def post(self, *args, **kwargs):
        request = self.request
        p_form = handymanProfileForm(request.POST, request.FILES,
                                        instance=request.user.handyman.handymanprofile)
        form = handymanForm(request.POST, instance=request.user.handyman)
        if form.is_valid() and p_form.is_valid():
            form.save()
            instance = p_form.save(commit=False)
            # This makes sure electrician does not change Service after selecting
            if request.user.handyman.handymanprofile.service:
                instance.service = request.user.handyman.handymanprofile.service
            instance.save()
            messages.success(request, 'profile updated successfully')
        else:
            return render(request, self.template_name, {"p_form": p_form, "form": form})
        return redirect("handyman:profile")


class ChangePasswordView(View):
    template_name = "handyman/change-password.html"

    def get(self, *arg, **kwargs):
        request = self.request
        form = PasswordChangeForm(request.User)
        return render(request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        request = self.request
        form = PasswordChangeForm(request.User, request.POST)
        if form.is_valid():
            User = form.save()
            update_session_auth_hash(request, User)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            return render(request, self.template_name, {"form": form})
        return redirect("handyman:change-password")


class FeedBackView(View):
    template_name = "feedback.html"

    def get(self, *arg, **kwargs):
        request = self.request
        form = handymanFeedbackForm()
        return render(request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        request = self.request
        form = handymanFeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.User = request.User.handyman
            if handymanFeedback.objects.filter(User=instance.User, subject=instance.subject, message=instance.message
                                                  ).exists():
                messages.info(request, f"Sorry, {instance.subject} has already been sent.")
            else:
                instance.save()
                messages.success(request, 'feedback has been sent successfully.')
        else:
            return render(request, self.template_name, {"form": form})
        return redirect("handyman:feedback")


class AppointmentListView(ListView):
    template_name = "handyman/Appointment.html"

    def get_queryset(self):
        request = self.request
        object_list = Appointment.objects.filter(ClientService=request.User.handyman.handymanprofile.ClientService)
        return object_list

    def post(self, *args, **kwargs):
        request = self.request
        check = request.POST.get('check')
        if check is not None:
            instance = get_object_or_404(Appointment, id=check)
            instance = CheckAppointments.objects.get(Appointment=instance)
            instance.status = True
            instance.save()
            messages.success(request, f"Appointment has been Checked successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ClientServiceListView(View):
    template_name = "handyman/ClientService.html"

    def get(self, *args, **kwargs):
        request = self.request
        object_list = ClientService.objects.filter(ClientService=request.User.handyman.handymanprofile.ClientService)
     #   context = {'d_form': DepartureForm(), 'a_form': ArrivalForm(), 'object_list': object_list}
        return render(self.request, self.template_name)


class ElectricianListView(ListView):
    template_name = "handyman.html"

    def get_queryset(self):
        request = self.request
        object_list = handymanProfileForm.objects.filter(
            User_type="Electrician", handymanprofile__ClientService=request.User.handyman.handymanprofile.ClientService)
        return object_list


class LogoutView(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, f"You've logged out successfully.")
        return redirect("handyman:index")
