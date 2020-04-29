from django.db import models
from model_utils import Choices
from ..common.models import TimeStampMixin, Rating, Cluster
from ..customers.models import Customer
from ..companies.models import Company

class CompanyRating(Rating, TimeStampMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return "customer_id: {}, company_id: {}, rating: {}, type: {}"\
            .format(self.customer_id, self.company_id, self.rating, self.type)

class CompanyCluster(Cluster, TimeStampMixin):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return "{} cluster : {} in {}".format(self.type, self.company_id, self.cluster_id)

class CustomerCluster(Cluster, TimeStampMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return "{} cluster : {} in {}".format(self.type, self.customer_id, self.cluster_id)