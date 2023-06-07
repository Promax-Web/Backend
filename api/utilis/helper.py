import base64
import binascii
import os
from .paginator import Paginator

def code_decoder(code, decode=False):
    if decode:
        return base64.b64decode(code).decode()
    else:
        return base64.b64encode(f"{code}".encode("utf-8")).decode()


def generate_key(cls):
    return binascii.hexlify(os.urandom(cls)).decode()


def custom_paginator(request, queryset, page):
    limit = 20  # settings.PER_PAGE
    offset = (page - 1) * limit
    pagination = Paginator(request, page=page, per_page=limit, count=queryset.count())
    return {
        'meta': pagination.get_paginated_response(),
        'queryset': queryset[offset:offset + limit]
    }
