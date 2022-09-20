from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, forms

from manager.models import managerProfile, manager, Payment, managerFeedback


class managerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = manager
        fields = ['last_name', 'first_name', 'email', 'username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        user.is_active = False
        if commit:
            user.save()
        return user


class managerProfileForm(ModelForm):
    class Meta:
        model = managerProfile
        fields = ['image', 'gender', 'phone_number', 'country']


class managerForm(ModelForm):
    class Meta:
        model = manager
        fields = ['last_name', 'first_name', 'email']




class managerFeedbackForm(ModelForm):
    class Meta:
        model = managerFeedback
        fields = ['subject', 'message']


class managerAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None and not self.user_cache.is_manager:
            logout(self.request)
            raise forms.ValidationError('Invalid username or password', code='invalid login')
