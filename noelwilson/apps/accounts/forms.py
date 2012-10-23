from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django import forms
from noelwilson.apps.accounts.models import UserProfile
from noelwilson.apps.blog.models import Entry

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    def save(self, *args, **kwargs):
        user = super(RegisterForm, self).save(*args, **kwargs)
        UserProfile.objects.create(user = user, email= self.cleaned_data['email'])
        
        return user

