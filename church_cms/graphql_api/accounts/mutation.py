import graphene

from ..bases import ErrorOutput
from .types import DeviceType, DeviceInput, DeviceConsentInput
from ..decorators import device_header_required
from accounts.services import register_device, update_device_consent


class DeviceResponse(graphene.Union):
    class Meta:
        types = (DeviceType, ErrorOutput)


class RegisterDeviceMutation(graphene.Mutation):
    class Arguments:
        input = DeviceInput(required=True)

    Output = DeviceResponse

    @classmethod
    def mutate(cls, root, info, input):
        try:
            return register_device(attributes=dict(input))
        except ValueError as e:
            return ErrorOutput(errors={'message': str(e)})


class UpdateDeviceConsentMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = DeviceConsentInput(required=True)

    Output = DeviceResponse

    @classmethod
    @device_header_required
    def mutate(cls, root, info, id, input):
        try:
            return update_device_consent(device_id=int(id), consent=dict(input))
        except Exception as e:
            return ErrorOutput(errors={'message': str(e)})


class DeviceMutationsMixin:
    register_device = RegisterDeviceMutation.Field()
    update_device_consent = UpdateDeviceConsentMutation.Field()
