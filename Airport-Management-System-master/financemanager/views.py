from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView

from financemanager.forms import financemanagerAuthenticationForm, financemanagerFeedbackForm, financemanagerProfileForm, financemanagerForm, \
    financemanagerSignUpForm
from financemanager.models import financemanagerFeedback, Payment


class financemanagerLoginView(LoginView):
    template_name = "financemanager/login.html"
    authentication_form = financemanagerAuthenticationForm

    def form_valid(self, form):
        User = form.get_user()
        if User is not None:
            login(self.request, User)
            messages.success(self.request, f"Hi {User.get_full_name}, you've logged in successfully.")
        return redirect('financemanager:index')


class financemanagerSignUpView(CreateView):
    form_class = financemanagerSignUpForm
    template_name = "financemanager/register.html"

    def form_valid(self, form):
        User = form.save(commit=False)
        User.save()
        messages.success(self.request, f"Hi {User.get_full_name}, your account has been created successfully wait for "
                                       f"approval.")
        return redirect('financemanager:login')


class HomeView(View): 
    template_name = "financemanager/index.html"

    def get(self, *args, **kwargs):
        request = self.request
        context = {"pending_payments_count": Payment.objects.filter(financemanager=request.user.financemanager, is_confirmed=False),
                   "confirmed_payments_count": Payment.objects.filter(financemanager=request.user.financemanager, is_confirmed=True)}
        return render(self.request, self.template_name, context)


class ProfileView(View):
    template_name = "financemanager/profile.html"

    def get(self, *args, **kwargs):
        request = self.request
        p_form = financemanagerProfileForm(instance=request.User.financemanager.financemanagerprofile)
        form = financemanagerForm(instance=request.User.financemanager)
        return render(self.request, self.template_name, {"p_form": p_form, "form": form})

    def post(self, *args, **kwargs):
        request = self.request
        p_form = financemanagerProfileForm(request.POST, request.FILES,
                                    instance=request.User.financemanager.financemanagerprofile)
        form = financemanagerForm(request.POST, instance=request.User.financemanager)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, 'profile updated successfully')
        else:
            return render(request, self.template_name, {"p_form": p_form, "form": form})
        return redirect("financemanager:profile")


class ChangePasswordView(View):
    template_name = "financemanager/change-password.html"

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
        return redirect("financemanager:change-password")


class FeedBackView(View):
    template_name = "financemanager/feedback.html"

    def get(self, *arg, **kwargs):
        request = self.request
        form = financemanagerFeedbackForm()
        return render(request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        request = self.request
        form = financemanagerFeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.User = request.User.financemanager
            if financemanagerFeedback.objects.filter(User=instance.User, subject=instance.subject, message=instance.message
                                              ).exists():
                messages.info(request, f"Sorry, {instance.subject} has already been sent.")
            else:
                instance.save()
                messages.success(request, 'feedback has been sent successfully.')
        else:
            return render(request, self.template_name, {"form": form})
        return redirect("financemanager:feedback")


class PaymentListView(ListView):
    template_name = "financemanager/payments.html"

    def get_queryset(self):
        request = self.request
        object_list = Payment.objects.filter(financemanager=request.user.financemanager)
        return object_list

    def post(self, *args, **kwargs):
        request = self.request
        confirm = request.POST.get('confirm')
        if confirm is not None:
            instance = get_object_or_404(Payment, id=confirm)
            instance.is_confirmed = True
            instance.save()
            Appointment = instance.Appointment
            Appointment.paid = True
            Appointment.save()
            messages.success(request, f"Payment has been confirmed successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LogoutView(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, f"You've logged out successfully.")
        return redirect("financemanager:index")

