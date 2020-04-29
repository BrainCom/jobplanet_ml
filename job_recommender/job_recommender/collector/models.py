from django.db import models
from ..common.models import TimeStampMixin
from ..customers.models import Customer
from ..companies.models import Company

class CompanyPageView(TimeStampMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    landing = models.PositiveIntegerField(default=0)
    review = models.PositiveIntegerField(default=0)
    salary = models.PositiveIntegerField(default=0)
    interview = models.PositiveIntegerField(default=0)
    job_posting = models.PositiveIntegerField(default=0)
    job_posting_detail = models.PositiveIntegerField(default=0)
    benefit = models.PositiveIntegerField(default=0)
    analytics = models.PositiveIntegerField(default=0)
    etc = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{} > {} : {}".format(self.customer_id, self.company_id, self.total)