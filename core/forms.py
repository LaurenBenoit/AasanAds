from django import forms
from core.models import LOCATION
import core.models as coremodels
class AdCreateForm(forms.ModelForm):
	location = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
											choices=LOCATION)

	class Meta:
		model = coremodels.Ad
		fields = ['title', 'description', 'phone_number', 'address', 'link_url', 'button_label', 'contact_preference']