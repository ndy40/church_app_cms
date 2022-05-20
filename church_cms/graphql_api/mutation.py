import graphene

from .accounts.mutation import RegisterDeviceMutation


class Mutation(graphene.ObjectType, RegisterDeviceMutation):
    pass
