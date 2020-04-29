import os
from tqdm import tqdm
import pandas as pd
import datetime
import decimal
from django.utils import timezone
from ...customers.models import Customer
from ...companies.models import Company
from ...analytics.models import CompanyRating

BATCH_SIZE = 900
DATA_DIR="job_recommender/builder/scripts/data/"
MAX_COMPANY = Company.objects.latest('id').id

def create_rating(uid, cid, score, timestamp = None):
    if timestamp:
        timestamp = datetime.datetime.fromtimestamp(float(timestamp))
    else:
        timestamp = timezone.now()

    company = Company.objects.get_or_create(id=cid)[0]
    customer = Customer.objects.get_or_create(id=uid)[0]
    rating = CompanyRating(customer=customer, company=company, rating=decimal.Decimal(score), rating_timestamp=timestamp)
    # rating = CompanyRating(customer_id=uid, company_id=cid, rating=decimal.Decimal(score), rating_timestamp=timestamp)

    return rating


def delete_db():
    print('truncate db')
    CompanyRating.objects.all().delete()
    print('finished truncate db')


def populate():
    df = pd.read_csv(DATA_DIR + "rating.csv", delimiter="\t", names=["uid", "cid", "score"])
    df = df.drop_duplicates(['uid','cid'])
    print('rating data loaded')

    bulk_list = []
    for (uid, cid, score) in tqdm(df.values.tolist()):
        if cid <= MAX_COMPANY:
            rating = create_rating(uid, cid, score)
            bulk_list.append(rating)

        if uid % BATCH_SIZE == 0:
            CompanyRating.objects.bulk_create(bulk_list)
            bulk_list = []


def run():
    print("Starting Rating Population script...")
    delete_db()
    populate()