from django.db import models
from ..common.models import TimeStampMixin
from ..customers.models import Occupation
from ..companies.models import Company

class Posting(TimeStampMixin):
    name = models.CharField(max_length=128)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    def __str__(self):
        return self.name

class PostingOccupation(TimeStampMixin):
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)

    def __str__(self):
        return self.posting_id