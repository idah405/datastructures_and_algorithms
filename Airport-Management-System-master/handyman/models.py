from multiprocessing.connection import Client
from django.db import models

# Create your models here.
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from Users.models import User, Profile, Feedback
from flights.models import service
from client.models import client


class handyman(User):
    class UserType(models.TextChoices):
        ELECTRICIAN = 'ELECTRICIAN', "ELECTRICIAN"
        PAINTERS = 'PAINTERS', "PAINTERS"
        TRANSPORTERS = 'TRANSPORTERS', "TRANSPORTERS"
        FUMIGANTS ='FUMIGANTS', "FUMIGANTS"
        


    User_type = models.CharField(max_length=250, choices=UserType.choices, default=UserType.ELECTRICIAN)

    class Meta:
        verbose_name = 'handyman'
        verbose_name_plural = 'handyman'


class handymanProfile(Profile):
    User = models.OneToOneField(handyman, on_delete=models.CASCADE)
    service = models.ForeignKey(service, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'handyman Profile'
        verbose_name_plural = 'handyman Profiles'


class handymanFeedback(Feedback):
    User = models.ForeignKey(handyman, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'handyman Feedback'
        verbose_name_plural = 'handyman Feedback'


class CheckAppointments(models.Model):
    status = models.BooleanField(default=False)
    handyman = models.ForeignKey(handyman, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(client,on_delete=models.CASCADE, null=True)
    #ticket = models.OneToOneField(Booking, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)

