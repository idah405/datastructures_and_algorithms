from autoslug import AutoSlugField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from flights.models import Appointment
from client.models import client
from financemanager.models import Payment
from Users.models import User, Profile, Feedback


class manager(User):
    pass

    class Meta:
        verbose_name = 'manager'
        verbose_name_plural = 'managers'


class managerProfile(Profile):
    User = models.OneToOneField(manager, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'manager Profile'
        verbose_name_plural = 'managers Profile'


class managerFeedback(Feedback):
    User = models.ForeignKey(manager, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'manager Feedback'
        verbose_name_plural = 'manager Feedback'


class served(models.Model):
    Appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    client = models.ForeignKey(client, on_delete=models.CASCADE, null=True)
    manager = models.ForeignKey(manager, on_delete=models.CASCADE, help_text="management officer", null=True)
    Payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    is_confirmed = models.BooleanField(default=False)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)



