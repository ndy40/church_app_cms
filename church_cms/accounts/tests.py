from django.test import TestCase
from django.db.models import QuerySet

from .models import Device, DeviceConsent, User

# Create your tests here.


class DeviceAndUserTestCase(TestCase):

    def test_create_device_success(self):
        new_device = Device.objects.create(token='token1', os_version='1.0.23', model='iPhone 6s',
                                           resolution='1080p', app_version='1.0.1', manufacturer='Apple')
        assert isinstance(new_device, Device)

    def test_create_device_with_consent(self):
        new_device = Device.objects.create(token='token1', os_version='1.0.23', model='iPhone 6s',
                                           resolution='1080p', app_version='1.0.1', manufacturer='Apple')
        consent = DeviceConsent(push_broadcast=True, app_notification=True, email=True, device=new_device)
        consent.save()

        assert isinstance(new_device.consent, DeviceConsent)

    def test_create_device_and_user_with_consent(self):
        user = User.objects.create_user(username='user1', email='user1@mail.com', password='password1')

        new_device = Device.objects.create(token='token1', os_version='1.0.23', model='iPhone 6s',
                                           resolution='1080p', app_version='1.0.1', manufacturer='Apple', user=user)
        consent = DeviceConsent(push_broadcast=True, app_notification=True, email=True, device=new_device)
        consent.save()

        assert new_device.user.username == 'user1'
        assert new_device.user.email == 'user1@mail.com'

    def test_detach_user_from_device(self):
        user = User.objects.create_user(username='user1', email='user1@mail.com', password='password1')

        new_device = Device.objects.create(token='token1', os_version='1.0.23', model='iPhone 6s',
                                           resolution='1080p', app_version='1.0.1', manufacturer='Apple', user=user)

        consent = DeviceConsent(push_broadcast=True, app_notification=True, email=True, device=new_device)
        consent.save()

        new_device.user = None
        new_device.save()

        assert new_device.user is None

    def test_get_all_user_devices(self):
        user = User.objects.create_user(username='user1', email='user1@mail.com', password='password1')

        new_device1 = Device.objects.create(token='token1', os_version='1.0.23', model='iPhone 6s',
                                            resolution='1080p', app_version='1.0.1', manufacturer='Apple', user=user)

        new_device2 = Device.objects.create(token='token2', os_version='1.0.23', model='iPhone 6s',
                                            resolution='1080p', app_version='1.0.1', manufacturer='Apple', user=user)

        for device in user.device_set.all():
            assert isinstance(device, Device)
