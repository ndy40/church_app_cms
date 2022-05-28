import graphene
import graphql

from .types import DeviceType, DeviceInput, DeviceConsentInput
from accounts.services import register_device, update_device_consent


class RegisterDeviceMutation(graphene.Mutation):
    class Arguments:
        input = DeviceInput(required=True)

    device = graphene.Field(DeviceType)

    @staticmethod
    def mutate(root, info, input):
        try:
            instance = register_device(attributes=dict(input))
            return RegisterDeviceMutation(device=instance)
        except ValueError as e:
            raise graphql.GraphQLError(str(e))


class UpdateDeviceConsentMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = DeviceConsentInput(required=True)

    device = graphene.Field(DeviceType)

    @staticmethod
    def mutate(root, info, id, input):
        try:
            device = update_device_consent(device_id=int(id), consent=dict(input))
            return UpdateDeviceConsentMutation(device=device)
        except ValueError:
            pass


class DeviceMutationsMixin:
    register_device = RegisterDeviceMutation.Field()
    update_device_consent = UpdateDeviceConsentMutation.Field()
