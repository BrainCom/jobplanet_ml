import logging
from tqdm import tqdm
import pandas as pd
from ...companies.models import Company, Industry
from ...scores.models import CompanySimilarity
from ...algo.models import Algo
from ...algo.predictors.surprise_sim_item import SurpriseSimItem
from ...utils.helpers.list_helper import divide_chunks


BATCH_SIZE = 900
MODEL_NAME = 'sim_company'
MODEL_VERSION = 1

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger('Surprise Item simialarity calculator')


def precalc_model(**kwargs):
    industry_id = kwargs.get("industry_id", None)
    k = int(kwargs.get("k", 1000))
    model_dir = None

    if not industry_id or \
       not Industry.objects.filter(id=industry_id).exists():
       raise ValueError("valid industry_id is required")

    logger.info("Pre-calculate similar")
    algo = Algo.objects.get(name=f"{MODEL_NAME}_{industry_id}", version=MODEL_VERSION)
    if not algo.algo:
        return

    try:
        model_dir = algo.algo.path
    except Algo.DoesNotExist:
        logging.error("Algo does not exist")
    except Phone.DoesNotExist:
        logging.error("Phone does not exist")

    if model_dir:
        bulk_list = []
        sim_item = SurpriseSimItem(model_dir)
        max_company_id = len(sim_item.model.sim) - 1

        comp = Company.objects.filter(industry_id=industry_id, id__lte=max_company_id).values_list('id', flat=True)
        CompanySimilarity.objects.filter(source_id__in=comp).delete()

        for company_id in tqdm(comp):
            for sim in sim_item.predict(company_id, k):
                if sim['company_id'] in comp:
                    comp_sim=CompanySimilarity(source_id=company_id,
                                               target_id=sim['company_id'],
                                               similarity=sim['score'],
                                               formula='pearson')
                    bulk_list.append(comp_sim)

            
        chunked = list(divide_chunks(bulk_list, BATCH_SIZE))
        for ch in tqdm(chunked):
            CompanySimilarity.objects.bulk_create(ch)


def run(*args):
    obj = {}
    for i in args:
        k,v = i.split("=")
        obj[k] = v

    precalc_model(**obj)