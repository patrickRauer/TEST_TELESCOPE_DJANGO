from django.contrib import admin

from .models import Type, Target, CatalogItem


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'ra', 'dec', 'type')
    list_filter = ('type',)
    search_fields = ('name',)


@admin.register(CatalogItem)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'target',
        'filter',
        'exposure_time',
        'capture',
        'created_at',
        'updated_at',
    )
    list_filter = ('target', 'filter', 'created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'