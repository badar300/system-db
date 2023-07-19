from django import forms
from django.contrib.auth.models import User

class login(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(required=True)

    def clean_data(self):
        email = self.cleaned_data['username']
        user = User.objects.filter(username=email).count()
        if user == 0:
           raise forms.ValidationError("You are not aligible to access this page")
        return email
class addSystem(forms.Form):
    project_number = forms.CharField(required=False)
    project_name = forms.CharField(required=False)
    standard = forms.CharField(required=False)
    system_tag = forms.CharField(required=False)
    platform = forms.CharField(required=False)
    interface = forms.CharField(required=False)
    controller = forms.CharField(required=False)
    system_medium = forms.CharField(required=False)
    system_type = forms.CharField(required=False)
    equip_sec = forms.CharField(required=False)
    sequence_data = forms.CharField(required=False)
    # control_sec = forms.CharField(required=False)
    # stages_property = forms.CharField(required=False)
