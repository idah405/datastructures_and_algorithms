from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, forms

from financemanager.models import financemanagerProfile, financemanager, Payment, financemanagerFeedback


class financemanagerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = financemanager
        fields = ['last_name', 'first_name', 'email', 'username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_financemanager = True
        user.is_active = False
        if commit:
            user.save()
        return user


class financemanagerProfileForm(ModelForm):
    class Meta:
        model = financemanagerProfile
        fields = ['image', 'gender', 'phone_number', 'country']


class financemanagerForm(ModelForm):
    class Meta:
        model = financemanager
        fields = ['last_name', 'first_name', 'email']


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['mpesa', ]

    def clean_mpesa(self):
        mpesa = self.cleaned_data.get('mpesa')
        if len(mpesa) != 10:
            raise ValidationError("Mpesa code is invalid, please confirm")
        return mpesa


class financemanagerFeedbackForm(ModelForm):
    class Meta:
        model = financemanagerFeedback
        fields = ['subject', 'message']


class financemanagerAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None and not self.user_cache.is_financemanager:
            logout(self.request)
            raise forms.ValidationError('Invalid username or password', code='invalid login')
