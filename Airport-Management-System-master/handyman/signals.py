from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from flights.models import Appointment
from handyman.models import handyman, handymanProfile, CheckAppointments


@receiver(post_save, sender=handyman)
def handyman_profile(sender, instance, created, **kwargs):
    if created:
        handymanProfile.objects.create(User=instance)
        instance.handymanProfile.save()


@receiver(post_save, sender=Appointment)
def check(sender, instance, created, **kwargs):
    if created:
        # this ensures only attendants in same plane as passenger can check passenger bookings
        Electrician = Appointment.objects.alias(entries=Count('CheckAppointment')).filter(
            user_type="electrician", is_active=True, handymanprofile__service=instance.ClientService.service).order_by(
            'entries').first()
        if Electrician:
            CheckAppointments.objects.create(ticket=instance, Electrician=Electrician)
            instance.CheckAppointment.save()
