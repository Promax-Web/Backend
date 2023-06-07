from django.db import models


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    icon = models.ImageField(blank=True, null=True)
    icon_svg = models.ImageField()
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    description_uz = models.CharField(max_length=300, blank=True, null=True)
    description_ru = models.CharField(max_length=300, blank=True, null=True)

    def str(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    description_uz = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    attributes = models.JSONField(blank=True, null=True, default=dict)

    def str(self) -> str:
        return self.title

    def __str__(self):
        return self.title_uz


class ProductImage(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    imgage = models.ImageField(upload_to='product/images/')



class Characteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)

    def str(self) -> str:
        return f"{self.product.title_uz} - {self.title_uz}"


class CharacteristicItem(models.Model):
    characteristic = models.ForeignKey(Characteristic, on_delete=models.SET_NULL, null=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def str(self) -> str:
        return self.title
