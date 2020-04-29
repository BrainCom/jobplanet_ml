from django.urls import path

from job_recommender.builder.views import (
	sync_all,
	sync_posting,
	sync_customer,
	sync_company,
	sync_collector,
	sync_rating,
	train_calc_similar_company,
	collect_rate_companyview,
	test,
)

app_name = "builder"
urlpatterns = [
    path("test/", view=test, name="test"),
    path("collect_rate_companyview/", view=collect_rate_companyview, name="collect_rate_companyview"),
    path("train_calc_similar_company/", view=train_calc_similar_company, name="train_calc_similar_company"),
    path("sync_all/", view=sync_all, name="sync_all"),
    path("sync_posting/", view=sync_posting, name="sync_posting"),
    path("sync_customer/", view=sync_customer, name="sync_customer"),
    path("sync_company/", view=sync_company, name="sync_company"),
    path("sync_collector/", view=sync_collector, name="sync_collector"),
    path("sync_rating/", view=sync_rating, name="sync_rating")
]
