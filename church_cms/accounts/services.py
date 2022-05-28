from django.forms import inlineformset_factory
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Device, DeviceConsent
from .forms import DeviceForm, DeviceConsentForm


def register_device(attributes: dict) -> Device:
    device_form = DeviceForm(attributes)

    if device_form.is_valid():
        instance = device_form.save()
        instance.consent = DeviceConsent(**attributes.get('consent'))
        instance.save()
        return instance

    if device_form.errors:
        raise ValueError(device_form.errors.get_json_data())


@receiver(signal=post_save, sender=Device)
def create_consent_on_device_create(sender, instance, created, **kwargs):
    if created:
        DeviceConsent.objects.create(device=instance)

    instance.consent.save()


def update_device_consent(device_id: int, consent: dict):
    if model := Device.objects.get(pk=device_id):
        if not hasattr(model, 'consent'):
            device_consent = DeviceConsent.objects.create(device=model)
            model.consent = device_consent

        for field, value in consent.items():
            setattr(model.consent, field, value)

        model.save()
        return model


def authenticate_device(token: str):
    """ query device table for token, first validate the token is valid.
    If found generated jwt token"""
    ...
