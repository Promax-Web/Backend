from rest_framework import serializers
from django.core.cache import cache
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    title = serializers.CharField(allow_blank=True, default='')
    description = serializers.CharField(allow_blank=True, default='')

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        super().__init__(*args, **kwargs)
        self.context.update(context)

    class Meta:
        model = Category
        fields = ("id", 'icon', 'icon_svg', 'title', 'description', 'children')

    def get_children(self, obj):
        serializer = self.__class__(obj.children.all(), many=True, context=self.context)
        return serializer.data
    
    def to_representation(self, instance):
        res = super().to_representation(instance)
        if self.context['lang'] == 'uz':
            res.update({
                'title': instance.title_uz,
                'description': instance.description_uz,
            })
        else:
            res.update({
                'title': instance.title_ru,
                'description': instance.description_ru,
            })
        return res

