from re import sub
from django import forms
from .models import Contacts, PREFIX_CHOICES, SUFFIX_CHOICES, STATE_CHOICES, DAY_CHOICES, CARRIER_CHOICES, ALERT_CHOICES, ALERT_TIMES, CURRENT_CHOICES
#Model Forms
class ContactForm(forms.ModelForm):

    #This statement controls whether the validation forces the field to be populated.  stackoverflow.coom/questions/16205908/django-modelform-not-required-field

    prefix=forms.CharField(required=True, max_length=5, widget=forms.Select(choices=PREFIX_CHOICES))
    first_name=forms.RegexField(regex=r'^[a-zA-Z\.\-\' ]+$')    
    last_name=forms.RegexField(regex=r'^[a-zA-Z\.\-\' ]+$')    
    suffix=forms.CharField(required=False, max_length=5, widget=forms.Select(choices=SUFFIX_CHOICES))
    address=forms.RegexField(regex=r'^[0-9a-zA-Z\.\-\' ]+$')    
    address2=forms.RegexField(required=False, regex=r'^[0-9a-zA-Z\.\-\' ]+$')    
    city=forms.RegexField(regex=r'^[a-zA-Z\.\-\' ]+$')    
    state=forms.CharField(required=True, max_length=2, widget=forms.Select(choices=STATE_CHOICES))
    carrier=forms.CharField(required=True, max_length=3, widget=forms.Select(choices=CARRIER_CHOICES))
    alert_day = forms.IntegerField(required=True, widget=forms.Select(choices=ALERT_CHOICES))
    alert_time =forms.TimeField(required=False, widget=forms.Select(choices=ALERT_TIMES))
    email_alert=forms.BooleanField(required=False, widget=forms.CheckboxInput)
    sms_alert=forms.BooleanField(required=False, widget=forms.CheckboxInput)
    terms=forms.BooleanField(error_messages={'required': 'You must accept the Terms of Use'}, label="Terms of Use")
    mobile=forms.RegexField(regex=r'^\s*1?[- (]*[0-9]{3}[- )]*[0-9]{3}[- ]*[0-9]{4}\s*$')    

    def clean_mobile(self):
        number = self.cleaned_data['mobile']
        number_str = sub('[^0-9]', '', number.strip().lstrip("1"))
        if len(number_str) == 10:
            return int(number_str)
        else:
            raise forms.ValidationError("Please enter a mobile number in the form 8005551212")
            return number

    class Meta:
        model = Contacts
        fields = [
                'prefix', 
                'first_name',
                'last_name',
                'suffix',
                'address',
                'address2',
                'city',
                'state',
                'zip',
                'email',
                'mobile',
            'carrier',
            'alert_day',
            'alert_time',
            'email_alert',
            'sms_alert',
            'terms'
        ]


class LookupForm(forms.ModelForm):

    #This statement controls whether the validation forces the field to be populated.  stackoverflow.com/questions/16205908/django-modelform-not-required-field

    municipality=forms.CharField(required=False, max_length=25, widget=forms.Select(choices=CURRENT_CHOICES))
    address=forms.RegexField(regex=r'^[0-9a-zA-Z\.\-\' ]+$')    
    zip=forms.RegexField(regex=r'^\d{5}$')    
   
    class Meta:
        model = Contacts
        fields = [
                'municipality',
                'address',
                'zip',
        ]

class CancelForm(forms.ModelForm):

    #Cancel based on email and mobile

    mobile=forms.RegexField(regex=r'^\d{10}$')    
   
    class Meta:
        model = Contacts
        fields = [
                'email',
                'mobile'
        ]

