from django.db import models
from ..common.models import TimeStampMixin

class Occupation(TimeStampMixin):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class Customer(TimeStampMixin):
    name = models.CharField(max_length=128, blank=True)
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE, related_name='customer_level1', blank=True, null=True)
    occupation2 = models.ForeignKey(Occupation, on_delete=models.CASCADE, related_name='customer_level2', blank=True, null=True)

    def __str__(self):
        return self.name
