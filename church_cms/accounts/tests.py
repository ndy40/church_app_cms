from django.test import TestCase


from .models import Device, DeviceConsent, User
from .services import register_device, update_device_consent

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

    def test_register_device(self):
        payload = {
            'token': 'token123',
            'os_version': 'iOS 15.1',
            'manufacturer': 'Apple',
            'model': 'iPone 11',
            'app_version': 'v1.0.3',
            'consent': {
                'push_broadcast': True,
                'app_notification': True,
                'email': False,
            }
        }

        new_device = register_device(payload)
        assert new_device.id is not None
        assert isinstance(new_device.consent, DeviceConsent)

    def test_update_device_consent(self):
        payload = {
            'token': 'token123',
            'os_version': 'iOS 15.1',
            'manufacturer': 'Apple',
            'model': 'iPone 11',
            'app_version': 'v1.0.3',
            'consent': {
                'push_broadcast': True,
                'app_notification': True,
                'email': False,
            }
        }

        new_device = register_device(payload)
        device = update_device_consent(new_device.id, {'push_broadcast': False})

        assert device.consent.push_broadcast is False
        assert device.consent.app_notification is True
        assert device.consent.email is False
