
# Create your models here.
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from Users.models import User, Profile, Feedback


class client(User):
    pass

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'client'


class clientProfile(Profile):
    user = models.OneToOneField(client, on_delete=models.CASCADE)
    dob = models.DateField(help_text="Date Of Birth", null=True)

    class Meta:
        verbose_name = 'clientProfile'
        verbose_name_plural = 'clientProfile'


class clientFeedback(Feedback):
    user = models.ForeignKey(client, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'clientFeedback'
        verbose_name_plural = 'clientFeedback'


@receiver(post_save, sender=client)
def client_profile(sender, instance, created, **kwargs):
    if created:
        clientProfile.objects.create(user=instance)
        instance.clientprofile.save()
