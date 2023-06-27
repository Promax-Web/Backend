from django.contrib import admin

from .models import ProductImage, Product, Category, ProductPrice, Coloring


# Register your models here.


class ImgInline(admin.StackedInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ImgInline]


@admin.register(Category)
class CategorAdmin(admin.ModelAdmin):
    list_display = ("id", 'title_uz', "title_uz", "parent", 'subTitle_uz')

@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ("id", 'product', "price", "created_at")


@admin.register(Coloring)
class ColoringAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_uz', 'url')

admin.site.register(Product, ProductAdmin)
# admin.site.register(Category)