import os
import logging
from django.core.files import File
from surprise import KNNBaseline, Dataset, Reader, dump
from surprise.model_selection import cross_validate
import pandas as pd
from ...companies.models import Industry
from ...analytics.models import CompanyRating
from ...algo.models import Algo


MODEL_DIR = './model.pkl'
MODEL_NAME = 'sim_company'
MODEL_VERSION = 1

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger('Surprise Item simialarity calculator')

def train_model(**kwargs):
    industry_id = kwargs.get("industry_id", None)
    sample_size = kwargs.get("sample_size", None)
    rating_scale = int(kwargs.get("rating_scale", 10))

    if not industry_id or \
       not Industry.objects.filter(id=industry_id).exists():
       raise ValueError("valid industry_id is required")


    logger.info("Calculation of Surprise item similarity")
    logger.info("Fetch ratings from db")

    ratings = CompanyRating.objects.filter(company__industry_id=industry_id)
    if sample_size:
        ratings = ratings[:int(sample_size)]

    ratings = list(ratings.values('customer_id', 'company_id', 'rating'))
    # ratings = list(CompanyRating.objects.filter(company_id__in=[1,2,3]).values('customer_id', 'company_id', 'rating'))
    df = pd.DataFrame(ratings)
    logger.info("Load dataset from ratings")
    reader_params=dict(rating_scale=(1, rating_scale))

    reader = Reader(**reader_params)
    data = Dataset.load_from_df(df, reader)

    logger.info("Build trainset")
    trainset = data.build_full_trainset()

    logger.info("Fit trainset")
    sim_options = {'name': 'pearson_baseline', 'user_based': False}
    algo = KNNBaseline(sim_options=sim_options)
    algo.fit(trainset)

    logger.info("Cross Validate")
    predictions = cross_validate(algo, data, verbose=True)

    logger.info("Dump model")

    dump.dump(MODEL_DIR, predictions, algo)
    with open(MODEL_DIR, 'rb') as fi:
        algo, _ = Algo.objects.get_or_create(name=f"{MODEL_NAME}_{industry_id}", version=MODEL_VERSION)
        algo.algo = File(fi, name=os.path.basename(fi.name))
        algo.save()

    if os.path.exists(MODEL_DIR):
      os.remove(MODEL_DIR)

    return industry_id


def run(*args):
    obj = {}
    for i in args:
        k,v = i.split("=")
        obj[k] = v

    print(obj)
    train_model(**obj)