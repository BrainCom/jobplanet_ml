from django.db import models
from ..common.models import TimeStampMixin

class Industry(TimeStampMixin):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Company(TimeStampMixin):
    name = models.CharField(max_length=128)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='company_level1', blank=True, null=True)
    industry2 = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='company_level2', blank=True, null=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
