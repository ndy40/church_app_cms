from functools import wraps

import graphql

from accounts.models import Device
from .constants import DEVICE_HEADER_KEY, ERROR_DEVICE_NOTFOUND


def device_header_required(fn):
    @wraps(fn)
    def wrapper(cls, root, info, **kwargs):
        if DEVICE_HEADER_KEY in info.context.META:
            if Device.objects.filter(token=info.context.META.get(DEVICE_HEADER_KEY)).exists():
                return fn(cls, root, info, **kwargs)
        raise graphql.GraphQLError(message=ERROR_DEVICE_NOTFOUND, source=root)

    return wrapper
