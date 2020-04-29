from django.contrib import admin
from django.contrib.admin import RelatedOnlyFieldListFilter
from rangefilter.filter import DateRangeFilter
from .models import Customer, Occupation

@admin.register(Occupation)
class OccupationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent_id', 'created_at', 'updated_at']
    list_per_page = 20
    list_filter = (
        ('created_at', DateRangeFilter), 
        ('updated_at', DateRangeFilter),
        ('parent', RelatedOnlyFieldListFilter)
    )
     
    search_fields = ["id", "name"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    ordering = ['-updated_at']
     
    list_display = ['id', 'name', 'occupation_id', 'occupation2_id', 'created_at', 'updated_at']
    list_per_page = 20
    list_filter = (
        ('created_at', DateRangeFilter), 
        ('updated_at', DateRangeFilter),
        ('occupation', RelatedOnlyFieldListFilter),
        ('occupation2', RelatedOnlyFieldListFilter)
    )
     
    search_fields = ["id", "name"]