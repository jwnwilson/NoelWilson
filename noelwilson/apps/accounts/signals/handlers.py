from django.db.models.signals import post_save
from django.contrib.auth.models import User

def create_profile(sender, **kwargs):
    # Have to import here to avoid importing before app is initialized
    from noelwilson.apps.accounts.models import UserProfile
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()

post_save.connect(create_profile, sender=User)