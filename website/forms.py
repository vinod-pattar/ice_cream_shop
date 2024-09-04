from django import forms

from .models import Product, Enquiry
from authentication.models import Address

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['first_name', 'last_name', 'email', 'mobile', 'product', 'message']

    user = forms.CharField(required=False)

    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(),
        empty_label='Select Product',
        to_field_name='id'
    )


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['user', 'building_no', 'street_address_1', 'street_address_2', 'area', 'city', 'pin']

        widgets = {
            'user': forms.HiddenInput()
        }

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)  # Get the user from the kwargs
    #     super(AddressForm, self).__init__(*args, **kwargs)
    #     if user:
    #         self.fields['user'] = forms.HiddenInput(queryset=Address.objects.filter(user=user.id), widget=forms.HiddenInput(), initial=user.id)
    # # user = forms.ModelChoiceField(queryset=Address.objects.filter(user=user_id), widget=forms.HiddenInput(), initial=user_id)

    building_no = forms.CharField(max_length=50, label='Building No', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Building No'}))
    street_address_1 = forms.CharField(max_length=100, label='Street Address 1', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address 1'}))
    street_address_2 = forms.CharField(max_length=100, label='Street Address 2', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address 2 (Optional)'}))
    area = forms.CharField(max_length=100, label='Area', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Area'}))
    city = forms.CharField(max_length=50, label='City', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    pin = forms.CharField(max_length=6, label='PIN', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PIN'}))