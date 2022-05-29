import graphene

from .accounts.mutation import DeviceMutationsMixin


class Mutation(graphene.ObjectType, DeviceMutationsMixin):
    pass
