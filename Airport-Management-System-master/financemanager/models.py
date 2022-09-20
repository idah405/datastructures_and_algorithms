from autoslug import AutoSlugField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from flights.models import Appointment
from client.models import client
from Users.models import User, Profile, Feedback


class financemanager(User):
    pass

    class Meta:
        verbose_name = 'financemanager'
        verbose_name_plural = 'Financesmanagers'


class financemanagerProfile(Profile):
    User = models.OneToOneField(financemanager, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'financemanager Profile'
        verbose_name_plural = 'financemanagers Profile'


class financemanagerFeedback(Feedback):
    User = models.ForeignKey(financemanager, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'financemanager Feedback'
        verbose_name_plural = 'financemanager Feedback'


class Payment(models.Model):
    slug = AutoSlugField(populate_from='code')
    code = models.CharField(max_length=20)
    Appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    client = models.ForeignKey(client, on_delete=models.CASCADE, null=True)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    mpesa = models.CharField(max_length=100, help_text="This is the M-Pesa Code for the transaction")
    financemanager = models.ForeignKey(financemanager, on_delete=models.CASCADE, help_text="Financemanager", null=True)
    is_confirmed = models.BooleanField(default=False)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)



