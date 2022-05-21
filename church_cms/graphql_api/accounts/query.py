import graphene

from accounts.models import Device

from .types import DeviceType


class DeviceQuery:
    devices = graphene.List(DeviceType)

    @staticmethod
    def resolve_devices(root, info, **kwargs):
        return Device.objects.all()
