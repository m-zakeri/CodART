from django.contrib import admin

from index.models import Refactoring, Parameter


@admin.register(Refactoring, Parameter)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]
