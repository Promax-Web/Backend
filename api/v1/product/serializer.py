from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductPrice, Characteristic, Coloring


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    title = serializers.CharField(allow_blank=True, default='')
    description = serializers.CharField(allow_blank=True, default='')
    subTitle = serializers.CharField(allow_blank=True, default='')

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        super().__init__(*args, **kwargs)
        self.context.update(context)

    class Meta:
        model = Category
        fields = ("id", 'icon', 'icon_svg', 'title', 'description', 'children', 'subTitle')

    def get_children(self, obj):
        serializer = self.__class__(obj.children.all(), many=True, context=self.context)
        return serializer.data

    def to_representation(self, instance):
        res = super().to_representation(instance)
        lang = self.context['lang']
        title_key = 'title_uz' if lang == 'uz' else 'title_ru'
        description_key = 'description_uz' if lang == 'uz' else 'description_ru'
        subTitle_key = 'subTitle_uz' if lang == 'uz' else 'subTitle_ru'
        res.update({
            'title': getattr(instance, title_key),
            'description': getattr(instance, description_key),
            'subTitle': getattr(instance, subTitle_key)
        })
        return res


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True, default='')
    description = serializers.CharField(allow_blank=True, default='')
    images = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    characteristic = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        super().__init__(*args, **kwargs)
        self.context.update(context)

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'attributes', 'category', 'price', 'images', 'characteristic')

    def get_images(self, obj):
        images = ProductImage.objects.select_related('product').filter(product_id=obj.id)
        return ProductImagesSerializer(images, many=True).data

    def get_price(self, obj):
        price = ProductPrice.objects.filter(product_id=obj.id).last()
        return price.price

    def get_characteristic(self, obj):
        characteristic = Characteristic.objects.filter(product_id=obj.id)
        return CharacteristicSerializer(characteristic, many=True, context={
            'lang': self.context['lang']
        }).data

    def get_attributes(self, obj):
        lang = self.context['lang']
        attributes_key = 'attributes_uz' if lang == 'uz' else 'attributes_ru'
        if hasattr(obj, attributes_key):
            return getattr(obj, attributes_key)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        lang = self.context['lang']

        title_key = 'title_uz' if lang == 'uz' else 'title_ru'
        description_key = 'description_uz' if lang == 'uz' else 'description_ru'
        if hasattr(instance, title_key):
            res['title'] = getattr(instance, title_key)
        if hasattr(instance, description_key):
            res['description'] = getattr(instance, description_key)

        res['category'] = {
            "id": instance.category.id,
            "title": instance.category.title_uz if lang == 'uz' else instance.category.title_ru,
        }
        return res


class CharacteristicSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    title = serializers.CharField(allow_blank=True, default='')

    class Meta:
        model = Characteristic
        fields = ('id', 'children', 'title')

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        super().__init__(*args, **kwargs)
        self.context.update(context)

    def get_children(self, obj):
        serializer = self.__class__(obj.children.all(), many=True, context=self.context)
        return serializer.data

    def to_representation(self, instance):
        res = super().to_representation(instance)
        lang = self.context['lang']
        title_key = 'title_uz' if lang == 'uz' else 'title_ru'
        res.update({
            'title': getattr(instance, title_key),

        })
        return res


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True, default='')
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'price', 'category', 'title', 'image')

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        super().__init__(*args, **kwargs)
        self.context.update(context)

    def get_image(self, obj):
        images = ProductImage.objects.select_related('product').filter(product_id=obj.id)[0]
        return images.image.url

    def get_price(self, obj):
        price = ProductPrice.objects.filter(product_id=obj.id).last()
        return price.price

    def to_representation(self, instance):
        res = super().to_representation(instance)
        lang = self.context['lang']
        title_key = 'title_uz' if lang == 'uz' else 'title_ru'
        category_key = 'title_uz' if lang == 'uz' else 'title_ru'
        res.update({
            'title': getattr(instance, title_key),
            'category': getattr(instance, category_key),
        })
        return res


class CertificateProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True, default='')

    class Meta:
        model = Product
        fields = ('id', 'title', 'tex_specific', 'passport_safe_boolean', 'passport_safe_file',
                  'sgp', 'certificate_canceled', 'free_certificate',
                  'free_certificate', 'fire_certificate', 'canceled_text',
                  'class_danger', 'sez', 'climate_test'
                  )
    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        super().__init__(*args, **kwargs)
        self.context.update(context)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        lang = self.context['lang']
        title_key = 'title_uz' if lang == 'uz' else 'title_ru'

        res.update({
            'title': getattr(instance, title_key),
        })
        return res


class ColoringSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True, default='')

    class Meta:
        model = Coloring
        fields = ('id', 'title', 'image', 'url')


    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        super().__init__(*args, **kwargs)
        self.context.update(context)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        lang = self.context['lang']
        title_key = 'title_uz' if lang == 'uz' else 'title_ru'

        res.update({
            'title': getattr(instance, title_key),
        })
        return res
