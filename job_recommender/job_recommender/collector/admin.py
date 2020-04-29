from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from .models import CompanyPageView

@admin.register(CompanyPageView)
class CompanyPageViewAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'company_id', 'created_at', 'updated_at',
    				'landing', 'review', 'salary', 'interview', 'job_posting',
    				'job_posting_detail', 'benefit', 'analytics', 'etc', 'total']
    list_per_page = 40
    list_filter = (
        ('created_at', DateRangeFilter), 
        ('updated_at', DateRangeFilter)
    )
     
    search_fields = ["customer_id", "company_id"]