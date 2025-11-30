from django.contrib import admin
from .models import LifestyleData

@admin.register(LifestyleData)
class LifestyleDataAdmin(admin.ModelAdmin):
    list_display = ('user','date','steps','sleep_hours','calories')
    list_filter = ('user','date')

