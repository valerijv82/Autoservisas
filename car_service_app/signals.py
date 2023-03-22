from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


# Pakoregaves vartotoja, issaugomas ir profilis

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if not created:
        print('save_profile: %s' % instance)
        instance.userprofile.save()


# Sukurus vartotoja automatiskai sukuriamas ir profilis
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('CREATE_PROFILE: %s' % instance)
    if created:
        UserProfile.objects.create(user=instance)
        print('KWARGS: ', kwargs)
