from django import forms
import datetime
from django.core.exceptions import ValidationError

class RenewBookForm(forms.Form):
    renew_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renew_date(self):

        data = self.cleaned_data['renew_date']

        if data < datetime.date.today():
            raise ValidationError('Invalid Date -- The Date you entered is in the past')
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Invalid Date -- Cannot renew book due Date more than 3 weeks.')
        
        return data


class UpdateAuthor(forms.Form):

    rewnew_date_of_birth = forms.DateField(help_text='none')
    rewnew_date_of_death = forms.DateField(help_text='none')

    def clean_rewnew_date_of_birth(self):
        data = self.cleaned_data['rewnew_date_of_birth']
        return data


