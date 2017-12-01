import re
from django import forms
from choices import *


# forms go here


class PatientForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super(PatientForm, self).clean()

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if not first_name or not last_name:
            raise forms.ValidationError("First name and Last name must be provided!")
        return cleaned_data


class DemographicForm(forms.Form):
    social_security_number = forms.CharField(max_length=50, required=False)
    date_of_birth = forms.CharField(max_length=10, required=False)
    cell_phone = forms.CharField(max_length=20, required=False)
    home_phone = forms.CharField(max_length=20, required=False)
    email = forms.CharField(max_length=40, required=False)
    gender = forms.ChoiceField(choices=gender_choices, required=True)
    race = forms.ChoiceField(choices=race_choices, required=False)
    ethnicity = forms.ChoiceField(choices=ethnicity_choices, required=False)
    city = forms.CharField(max_length=100, required=False)
    state = forms.ChoiceField(choices=state_choices, required=False)
    zip_code = forms.IntegerField(required=False)

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(DemographicForm, self).clean()
        SSN = cleaned_data.get('social_security_number')
        Gender = cleaned_data.get('gender')
        # https://stackoverflow.com/questions/8022530/python-check-for-valid-email-address
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
        email_address = cleaned_data.get('email')

        if email_address and not EMAIL_REGEX.match(email_address):
            raise forms.ValidationError("Please provide a valid email address")
        if not Gender:
            raise forms.ValidationError("Gender must be specified")
        if SSN and len(str(SSN)) != 9:
            raise forms.ValidationError("Please enter a valid U.S. social security number")
        return cleaned_data







