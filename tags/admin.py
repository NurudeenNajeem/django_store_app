from django.contrib import admin
# from .models import Tag
from . import models

# Register your models here.
@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
     # list_display = ["label"]
     search_fields = ['tags']

# admin.site.register(Tag)
