from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from dpuser.models.UserProfile import UserProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if (created and instance.is_superuser):
        UserProfile.objects.get_or_create(user=instance)
    elif (created and instance.is_superuser == False):
        UserProfile.objects.get_or_create(user=instance, gender=instance.gender, dob=instance.dob, bio=instance.bio)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#     print(instance)
