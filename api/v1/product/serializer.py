from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductPrice



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
        lang = self.context['lang']
        title_key = 'title_uz' if lang == 'uz' else 'title_ru'
        description_key = 'description_uz' if lang == 'uz' else 'description_ru'
        res.update({
            'title': getattr(instance, title_key),
            'description': getattr(instance, description_key),
        })
        return res

class ProductCategoryFilterSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True, default='')
    price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        super().__init__(*args, **kwargs)
        self.context.update(context)

    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'price', 'image')

    def get_image(self, obj):
        image = ProductImage.objects.select_related('product').filter(product_id=obj.id).first()
        return ProductImagesSerializer(image).data

    def to_representation(self, instance):
        res = super().to_representation(instance)
        if self.context['lang'] == 'uz':
            res.update({
                'title': instance.title_uz,
            })
        else:
            res.update({
                'title': instance.title_ru,
            })
        res['category'] = CategorySerializer(instance.category, context={'lang': self.context['lang']}).data
        return res


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True, default='')
    description = serializers.CharField(allow_blank=True, default='')
    images = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        super().__init__(*args, **kwargs)
        self.context.update(context)

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'attributes', 'category', 'price', 'images')

    def get_images(self, obj):
        images = ProductImage.objects.select_related('product').filter(product_id=obj.id)
        return ProductImagesSerializer(images, many=True).data

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
        res['category'] = CategorySerializer(instance.category, context={'lang': self.context['lang']}).data


    def get_price(self, obj):
        price = ProductPrice.objects.filter(product_id=obj.id).last()
        return price.price

    def get_image(self, obj):
        image = ProductImage.objects.filter(product_id=obj.id).last().imgage
        return image.url
    
    # def to_representation(self, instance):
    #     res = super().to_representation(instance)
    #     lang = self.context['lang']
    #
    #     title_key = 'title_uz' if lang == 'uz' else 'title_ru'
    #     if hasattr(instance, title_key):
    #         res['title'] = getattr(instance, title_key)
    #     res['category'] = {
    #         "id": instance.category.id,
    #         "title": instance.category.title_uz if lang == 'uz' else instance.category.title_ru,
    #     }
    #     return res