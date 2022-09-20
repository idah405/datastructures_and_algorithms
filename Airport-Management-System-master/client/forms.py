from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, forms

from .models import client, clientProfile, clientFeedback


class clientSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = client
        fields = ['last_name', 'first_name', 'email', 'username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_client = True
        user.is_active = True
        if commit:
            user.save()
        return user


class clientProfileForm(ModelForm):
    class Meta:
        model = clientProfile
        fields = ['image', 'gender', 'phone_number', 'country']


class clientForm(ModelForm):
    class Meta:
        model = client
        fields = ['last_name', 'first_name', 'email']


class clientFeedbackForm(ModelForm):
    class Meta:
        model = clientFeedback
        fields = ['subject', 'message']


class clientAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None and not self.user_cache.is_client:
            logout(self.request)
            raise forms.ValidationError("Sorry you can't login here. Your account is not a client account.",
                                        code='invalid login')
