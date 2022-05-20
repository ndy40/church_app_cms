import graphene

from .accounts.query import DeviceQuery


class Query(graphene.ObjectType, DeviceQuery):
    pass
