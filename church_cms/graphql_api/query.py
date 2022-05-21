import graphene

from .accounts.query import DeviceQuery


class Query(graphene.ObjectType, DeviceQuery):
    hello = graphene.String(default_value='hi')
