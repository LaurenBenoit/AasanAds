from django import forms
from core.models import LOCATION
import core.models as coremodels
from django.core.validators import RegexValidator
class AdCreateForm(forms.ModelForm):
	location = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
											choices=LOCATION)

	class Meta:
		model = coremodels.Ad
		fields = ['title', 'description', 'phone_number', 'address', 'link_url', 'button_label', 'contact_preference']

class AdCloseForm(forms.ModelForm):
	location = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
											choices=LOCATION)	
	clicks_promised = forms.IntegerField()
	money_negotiated = forms.IntegerField()
	cnic_regex = RegexValidator(regex=r'^[0-9]{13,13}', message="enter 13 digits without dashes.")
	cnic = forms.CharField(validators=[cnic_regex], max_length=15)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+923334404403'.")
	phone_number = forms.CharField(validators=[phone_regex], max_length=20)
	class Meta:
		fields = ['title', 'description', 'address', 'link_url', 'button_label', 'contact_preference']
		model = coremodels.Ad

class AdUpdateForm(forms.ModelForm):
	location = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
											choices=LOCATION)
	class Meta:
		fields = ['title', 'description', 'address', 'link_url', 'button_label', 'contact_preference']
		model = coremodels.Ad


class AgentCreateForm(forms.ModelForm):
	location = forms.ChoiceField(widget=forms.Select(),
											choices=LOCATION, required=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = forms.CharField(validators=[phone_regex], max_length=20)
	first_name = forms.CharField(required = True, max_length=20)
	last_name = forms.CharField(required = True, max_length=20)
	class Meta:
		fields = ['username','password', 'first_name', 'last_name', ]
		model = coremodels.User

class DashboardKhoofiaForm(forms.ModelForm):
	numeric = RegexValidator(r'^[0-9]{5,5}$', 'Only 5 digit numeric field allowed.')
	khoofia = forms.CharField(required = True, validators = [numeric], max_length=5)
	class Meta:
		fields = ['khoofia']
		model = coremodels.Topup
