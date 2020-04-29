from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from .models import CustomerSimilarity, CompanySimilarity

class SimilarityAdmin(admin.ModelAdmin):
    list_display = ['id', 'formula', 'source_id', 'target_id', 'similarity', 'created_at', 'updated_at']
    list_per_page = 50
    list_filter = (
        ('created_at', DateRangeFilter), 
        ('updated_at', DateRangeFilter),
        ('formula', admin.AllValuesFieldListFilter)
    )
     
    search_fields = ["source_id", "target_id"]


admin.site.register(CustomerSimilarity, SimilarityAdmin)
admin.site.register(CompanySimilarity, SimilarityAdmin)