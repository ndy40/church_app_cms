import graphene

from .accounts.query import MeContextType


class Query(MeContextType, graphene.ObjectType):
    pass
