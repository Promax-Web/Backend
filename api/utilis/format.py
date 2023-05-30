from collections import OrderedDict


def category_format(data):
    return OrderedDict([
        ('id', data.id),
        ('title_uz', data.title_uz),
        ('title_ru', data.title_ru),
        ("description_uz", data.description_uz),
        ("description_ru", data.description_ru),
        ("logo", data.logo.url)
    ])
