from django.contrib import admin
from django.contrib.admin import RelatedOnlyFieldListFilter
from rangefilter.filter import DateRangeFilter
from .models import Company, Industry


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent_id', 'created_at', 'updated_at']
    list_per_page = 20
    list_filter = (
        ('created_at', DateRangeFilter), 
        ('updated_at', DateRangeFilter),
        ('parent', RelatedOnlyFieldListFilter)
    )
     
    search_fields = ["id", "name"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    ordering = ['-updated_at']
     
    list_display = ['id', 'name', 'industry_id', 'industry2_id', 
                    'confirmed', 'created_at', 'updated_at']
    list_per_page = 20
    list_filter = (
        ('created_at', DateRangeFilter), 
        ('updated_at', DateRangeFilter),
        ('industry', RelatedOnlyFieldListFilter),
        ('industry2', RelatedOnlyFieldListFilter)
    )
     
    search_fields = ["id", "name"]