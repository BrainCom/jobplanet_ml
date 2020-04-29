from django.db import models
from model_utils import Choices

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Similarity(models.Model):
    FORMULA = Choices('cosine', 'pearson')

    similarity = models.DecimalField(max_digits=8, decimal_places=7)
    formula = models.CharField(max_length=16, choices=FORMULA, default=FORMULA.cosine)

    class Meta:
        abstract = True
        

class Rating(models.Model):
    RATING = Choices('explicit', 'implicit')

    rating = models.DecimalField(decimal_places=2, max_digits=4)
    rating_timestamp = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=8, choices=RATING, default=RATING.implicit)

    class Meta:
        abstract = True


class Cluster(models.Model):
    CLUSTER = Choices('kmeans')

    cluster_id = models.PositiveIntegerField()
    type = models.CharField(max_length=8, choices=CLUSTER, default=CLUSTER.kmeans)

    class Meta:
        abstract = True