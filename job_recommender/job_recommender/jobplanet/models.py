from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from ..common.models import TimeStampMixin


class User(TimeStampMixin):
    name = models.CharField(db_column='fullname', max_length=128, blank=True, null=True)
    quit_at = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Occupation(TimeStampMixin):
    name = models.CharField(db_column='name_ko_kr', max_length=64)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    active = models.BooleanField(default=False)
    weight = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'occupations'

    def __str__(self):
        return self.name


class UserInfo(TimeStampMixin):
    QUESTION = Choices((130, 'latest_company', _('latest company')),
                       (144, 'latest_job_title', _('latest job title')), 
                       (133, 'latest_school', _('latest school')), 
                       (142, 'latest_major', _('latest major')), 
                       (132, 'years_of_experience', _('years of experience')),
                       (134, 'skill', _('skill')),
                       (147, 'occupation_level2', _('occupation')))

    question_id = models.IntegerField(choices=QUESTION, default=QUESTION.occupation_level2)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(db_column='other_text', max_length=128, blank=True, null=True)
    occupation = models.ForeignKey(Occupation, db_column='reference_id', on_delete=models.PROTECT, blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'goodjob_answers'

    def __str__(self):
        return self.name    


class Industry(TimeStampMixin):
    name = models.CharField(db_column='name_ko_kr', max_length=64)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    active = models.BooleanField(db_column='category_visible', default=False)

    class Meta:
        db_table = 'industries'

    def __str__(self):
        return self.name


class Company(TimeStampMixin):
    name = models.CharField(max_length=128)
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT, related_name='company_level1', blank=True, null=True)
    industry2 = models.ForeignKey(Industry, db_column='industry_level2_id', related_name='company_level2', on_delete=models.PROTECT, blank=True, null=True)
    review_avg_cache = models.DecimalField(decimal_places=2, max_digits=4)
    partners_confirmed_at = models.DateTimeField(db_column='next_data_mapping_at')

    class Meta:
        db_table = 'companies'

    def __str__(self):
        return self.name


class CompanyReference(TimeStampMixin):
    name = models.CharField(max_length=128)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    confirmed_at = models.DateTimeField(db_column='last_confirmed_at')

    class Meta:
        db_table = 'company_references'

    def __str__(self):
        return self.name

class JobPosting(TimeStampMixin):
    STATUS = Choices('PUBLISHED', 'DELETED','DRAFT')

    name = models.CharField(db_column='title', max_length=128)
    status = models.CharField(max_length=16, choices=STATUS, default=STATUS.PUBLISHED)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    class Meta:
        db_table = 'job_postings'

    def __str__(self):
        return self.name

class PostingOccupation(TimeStampMixin):
    posting = models.ForeignKey(JobPosting, on_delete=models.PROTECT)
    occupation = models.ForeignKey(Occupation, on_delete=models.PROTECT)

    class Meta:
        db_table = 'job_posting_occupations'

    def __str__(self):
        return self.posting_id
