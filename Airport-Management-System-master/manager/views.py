from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView

from manager.forms import managerAuthenticationForm, managerFeedbackForm, managerProfileForm, managerForm, \
managerSignUpForm
from manager.models import managerFeedback, served


class managerLoginView(LoginView):
    template_name = "manager/login.html"
    authentication_form = managerAuthenticationForm

    def form_valid(self, form):
        User = form.get_user()
        if User is not None:
            login(self.request, User)
            messages.success(self.request, f"Hi {User.get_full_name}, you've logged in successfully.")
        return redirect('manager:index')


class managerSignUpView(CreateView):
    form_class = managerSignUpForm
    template_name = "manager/register.html"

    def form_valid(self, form):
        User = form.save(commit=False)
        User.save()
        messages.success(self.request, f"Hi {User.get_full_name}, your account has been created successfully wait for "
                                       f"approval.")
        return redirect('manager:login')


class HomeView(View): 
    template_name = "manager/index.html"

    def get(self, *args, **kwargs):
        request = self.request
        context = {"pending_served_count": served.objects.filter(manager=request.user.manager, is_confirmed=False),
                   "confirmed_served_count": served.objects.filter(manager=request.user.manager, is_confirmed=True)}
        return render(self.request, self.template_name, context)


class ProfileView(View):
    template_name = "manager/profile.html"

    def get(self, *args, **kwargs):
        request = self.request
        p_form = managerProfileForm(instance=request.user.manager.managerProfile)
        form = managerForm(instance=request.User.manager)
        return render(self.request, self.template_name, {"p_form": p_form, "form": form})

    def post(self, *args, **kwargs):
        request = self.request
        p_form = managerProfileForm(request.POST, request.FILES,
                                    instance=request.User.manager.managerprofile)
        form = managerForm(request.POST, instance=request.User.manager)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, 'profile updated successfully')
        else:
            return render(request, self.template_name, {"p_form": p_form, "form": form})
        return redirect("manager:profile")


class ChangePasswordView(View):
    template_name = "manager/change-password.html"

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
        return redirect("manager:change-password")


class FeedBackView(View):
    template_name = "manager/feedback.html"

    def get(self, *arg, **kwargs):
        request = self.request
        form = managerFeedbackForm()
        return render(request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        request = self.request
        form = managerFeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.User = request.User.manager
            if managerFeedback.objects.filter(User=instance.User, subject=instance.subject, message=instance.message
                                              ).exists():
                messages.info(request, f"Sorry, {instance.subject} has already been sent.")
            else:
                instance.save()
                messages.success(request, 'feedback has been sent successfully.')
        else:
            return render(request, self.template_name, {"form": form})
        return redirect("manager:feedback")


class servedListView(ListView):
    template_name = "manager/served.html"

    def get_queryset(self):
        request = self.request
        object_list = served.objects.filter(manager=request.user.manager)
        return object_list

    def post(self, *args, **kwargs):
        request = self.request
        confirm = request.POST.get('confirm')
        if confirm is not None:
            instance = get_object_or_404(served, id=confirm)
            instance.is_confirmed = True
            instance.save()
            Appointment = instance.Appointment
            Appointment.paid = True
            Appointment.save()
            messages.success(request, f"client has been successfully served")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LogoutView(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, f"You've logged out successfully.")
        return redirect("manager:index")

