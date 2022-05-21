import graphene

from .types import DeviceType, DeviceInput, DeviceUpdate


class RegisterDeviceMutation:
    class Arguments:
        input = graphene.InputField(DeviceInput)

    register_device = graphene.Field(DeviceType)

    @classmethod
    def mutate(cls, root, info, input):
        pass
