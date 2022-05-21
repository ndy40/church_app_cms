import graphene
from graphene import InputObjectType
from graphene_django import DjangoObjectType

from accounts.models import Device, DeviceConsent, User


class DeviceType(DjangoObjectType):
    class Meta:
        model = Device
        fields = ('id', 'os_version', 'manufacturer', 'model', 'resolution', 'screen_height', 'screen_width',
                  'app_version', 'token', 'consent', 'user')


class DeviceConsentType(DjangoObjectType):
    class Meta:
        model = DeviceConsent
        fields = '__all__'


class DeviceInput(InputObjectType):
    manufacturer = graphene.Field(graphene.String, required=True)
    os_version = graphene.Field(graphene.String, required=True)
    model = graphene.Field(graphene.String, required=True)
    token = graphene.Field(graphene.String, required=True)
    consent = graphene.Field(DeviceConsent)


class DeviceUpdate(InputObjectType):
    manufacturer = graphene.Field(graphene.String)
    os_version = graphene.Field(graphene.String)
    model = graphene.Field(graphene.String)
    token = graphene.Field(graphene.String)
    consent = graphene.Field(DeviceConsent)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'birthday', 'is_member', 'first_name', 'last_name', 'date_joined', 'last_login')