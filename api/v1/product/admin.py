from django.contrib import admin

from .models import ProductImage, Product, Category


# Register your models here.


class ImgInline(admin.StackedInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ImgInline]


@admin.register(Category)
class CategorAdmin(admin.ModelAdmin):
    list_display = ("id", 'title_uz', "title_ru", "parent")

admin.site.register(Product, ProductAdmin)
# admin.site.register(Category)