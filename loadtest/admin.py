from django.contrib import admin
from .models import SoloPiFile, Product


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'producter', 'created_time')


@admin.register(SoloPiFile)
class SoloPiFileAdmin(admin.ModelAdmin):
    list_display = ('product', 'filename', 'filepath', 'created_time')
