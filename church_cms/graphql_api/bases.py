import graphene
from graphql_auth.bases import OutputErrorType


class ErrorOutput(graphene.ObjectType):
    errors = graphene.Field(OutputErrorType)
