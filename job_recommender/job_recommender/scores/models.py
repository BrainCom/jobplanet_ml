from django.db import models
from ..common.models import TimeStampMixin, Similarity
from ..customers.models import Customer
from ..companies.models import Company


class CustomerSimilarity(Similarity, TimeStampMixin):
    source = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sim_source')
    target = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sim_target')

    def __str__(self):
        return "<{}>[({} => {}) sim = {}]".format(self.formula,
                                                  self.source_id,
                                                  self.target_id,
                                                  self.similarity)

    class Meta:
        constraints = [
          models.UniqueConstraint(fields=['source_id', 'target_id'], name='unique_customer_sim')
        ]
        indexes = [
           models.Index(fields=['-similarity'])
        ]


class CompanySimilarity(Similarity, TimeStampMixin):
    source = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sim_source')
    target = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sim_target')

    def __str__(self):
        return "<{}>[({} => {}) sim = {}]".format(self.formula,
                                                  self.source_id,
                                                  self.target_id,
                                                  self.similarity)

    class Meta:
        constraints = [
          models.UniqueConstraint(fields=['source_id', 'target_id'], name='unique_company_sim')
        ]
        indexes = [
           models.Index(fields=['-similarity'])
        ]