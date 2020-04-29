from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from .models import CompanyRating, CompanyCluster, CustomerCluster


admin.site.register(CompanyCluster)
admin.site.register(CustomerCluster)

@admin.register(CompanyRating)
class CompanyRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'customer_id', 'company_id', 'rating', 'rating_timestamp', 'created_at', 'updated_at']
    list_per_page = 50
    list_filter = (
        ('created_at', DateRangeFilter), 
        ('updated_at', DateRangeFilter),
        ('type', admin.AllValuesFieldListFilter)
    )
     
    search_fields = ["customer_id", "company_id"]