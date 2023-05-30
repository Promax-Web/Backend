from django.contrib import admin

from .models import ProductImage, Product, Category


# Register your models here.


class ImgInline(admin.StackedInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ImgInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)