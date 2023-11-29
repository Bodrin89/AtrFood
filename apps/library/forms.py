from dal import autocomplete
from django import forms
from django.urls import reverse

from apps.library.models import AddressArtFood


class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressArtFood
        fields = '__all__'

        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete'),
            'district': autocomplete.ModelSelect2(url='district-autocomplete', forward=['city']),
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['district'].widget.attrs['data-autocomplete-dependency'] = 'city'
