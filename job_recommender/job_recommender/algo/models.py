import datetime
from django.db import models
from model_utils import Choices
from ..common.models import TimeStampMixin

def algo_directory_path(ins, filename):
    return 'algo/{0}/{1}/{2:%Y%m%d_%H%M%S}/{3}'.format(ins.name, 
                                                       ins.version,
                                                       datetime.datetime.now(),
                                                       filename)

class Algo(TimeStampMixin):
    TYPES = Choices('sim_company', 'sim_customer')

    name = models.CharField(max_length=64, choices=TYPES, default=TYPES.sim_company)
    version = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=128, blank=True)
    algo = models.FileField(upload_to=algo_directory_path)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
          models.UniqueConstraint(fields=['name', 'version'], name='unique_algo_name')
        ]
