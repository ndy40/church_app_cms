from django import forms

from .models import Device, DeviceConsent


class DeviceConsentForm(forms.ModelForm):
    class Meta:
        model = DeviceConsent
        fields = '__all__'
        exclude = ('device',)


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'
