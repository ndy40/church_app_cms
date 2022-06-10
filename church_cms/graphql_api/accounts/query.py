import graphene

from accounts.models import Device

from ..constants import DEVICE_HEADER_KEY
from ..decorators import device_header_required
from .types import MeContextType


class MeContext:
    me = graphene.Field(MeContextType)

    @classmethod
    @device_header_required
    def resolve_me(cls, root, info):
        payload = dict()

        if DEVICE_HEADER_KEY in info.context.META:
            device = Device.objects.get(token=info.context.META.get(DEVICE_HEADER_KEY))
            payload['device'] = device

        return MeContextType(**payload)
