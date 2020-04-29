from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from .models import Algo


@admin.register(Algo)
class AlgoAdmin(admin.ModelAdmin):
    ordering = ['-updated_at']
     
    list_display = ['id', 'name', 'version', 'created_at', 'updated_at']
    list_per_page = 20
    list_filter = (
        ('created_at', DateRangeFilter), 
        ('updated_at', DateRangeFilter)
    )
     
    search_fields = ["name"]