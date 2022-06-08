from django import forms
from django.core.exceptions import ValidationError
from .models import UserProfiles


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfiles
        fields = ['useridx', 'fullname', 'avatar', 'phone', 'email']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['avatar'].required = False
        self.fields['useridx'].widget = forms.HiddenInput()
        self.fields['useridx'].required = False

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if phone < 10000000:
                raise ValidationError(message='Phone number must be at least 8 characters long')
            if UserProfiles.objects.exclude(useridx=self.cleaned_data['useridx']).filter(phone=phone).exists():
                raise ValidationError(message='User with this phone is already registered')
            return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserProfiles.objects.exclude(useridx=self.cleaned_data['useridx']).filter(email=email).exists():
            raise ValidationError(message='User with this email is already registered')
        return email
