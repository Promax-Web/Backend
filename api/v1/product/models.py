from django.db import models


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    icon = models.ImageField(blank=True, null=True)
    icon_svg = models.ImageField()
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    description_uz = models.CharField(max_length=300, blank=True, null=True)
    description_ru = models.CharField(max_length=300, blank=True, null=True)
    subTitle_uz = models.CharField(max_length=300, null=True, blank=True)
    subTitle_ru = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title_uz

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.subTitle_uz = self.title_uz.replace(" ", "_")
        if self.title_ru:
            self.subTitle_ru = self.title_ru.replace(" ", "_")
        super().save(*args, **kwargs)


class Product(models.Model):
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    description_uz = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    attributes_uz = models.JSONField(blank=True, null=True, default=dict)
    attributes_ru = models.JSONField(blank=True, null=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.title_uz


class ProductImage(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='product/images/')


class Characteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)

    def str(self) -> str:
        return f"{self.product.title_uz} - {self.title_uz}"


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)