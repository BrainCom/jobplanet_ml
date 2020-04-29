from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from .models import Posting, PostingOccupation


@admin.register(PostingOccupation)
class PostingOccupationAdmin(admin.ModelAdmin):
    list_display = ['id', 'posting_id', 'occupation_id', 'created_at', 'updated_at']
    list_per_page = 20
    list_filter = (
        ('created_at', DateRangeFilter), 
        ('updated_at', DateRangeFilter)
    )
     
    search_fields = ["posting_id", "occupation_id"]


@admin.register(Posting)
class PostingAdmin(admin.ModelAdmin):
    ordering = ['-updated_at']
     
    list_display = ['id', 'name', 'company_id', 'start_at', 'end_at', 'created_at', 'updated_at']
    list_per_page = 20
    list_filter = (
        ('created_at', DateRangeFilter), 
        ('updated_at', DateRangeFilter),
        ('start_at', DateRangeFilter), 
        ('end_at', DateRangeFilter)
    )
     
    search_fields = ["name", "company_id"]