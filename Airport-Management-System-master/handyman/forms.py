from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, forms

from handyman.models import handyman, handymanProfile, handymanFeedback


class handymanSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = handyman
        fields = ['last_name', 'first_name', 'email', 'username', 'User_type']

    def save(self, commit=True):
        User = super().save(commit=False)
        User.is_handyman = True
        User.is_active = False
        if commit:
            User.save()
        return User


class handymanProfileForm(ModelForm):
    class Meta:
        model = handymanProfile
        fields = ['image', 'gender', 'phone_number', 'country', 'service']


class handymanForm(ModelForm):
    class Meta:
        model = handyman
        fields = ['last_name', 'first_name', 'email']


class handymanFeedbackForm(ModelForm):
    class Meta:
        model = handymanFeedback
        fields = ['subject', 'message']


class handymanAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None and not self.user_cache.is_handyman:
            logout(self.request)
            raise forms.ValidationError("Sorry invalid credentials.",
                                        code='invalid login')



