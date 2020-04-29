import os
from tqdm import tqdm
import pandas as pd
from ...companies.models import Company, Industry

BATCH_SIZE = 900
DATA_DIR="job_recommender/builder/scripts/data/"
INDUSTRY = [
    ["서비스업", 100, 27874],
    ["제조/화학", 200, 124376],
    ["의료/제약/복지", 300,   6945],
    ["유통/무역/운송", 400, 72671],
    ["교육업", 500, 5554],
    ["건설업", 600, 60979],
    ["IT/웹/통신", 700, 26194],
    ["미디어/디자인", 800, 13490],
    ["은행/금융업", 900, 7684],
    ["기관/협회", 1000  , 10661]
]
INDUSTRY_NICE_CONFIRMED = [
    ["서비스업", 100, 1019],
    ["제조/화학", 200, 4470],
    ["의료/제약/복지", 300, 389],
    ["유통/무역/운송", 400, 2288],
    ["교육업", 500, 292],
    ["건설업", 600, 982],
    ["IT/웹/통신", 700, 3017],
    ["미디어/디자인", 800, 1163],
    ["은행/금융업", 900, 578],
    ["기관/협회", 1000, 815]
]

def create_company(id, name, industry):
    company = Company(id=id)
    company.name = name

    if industry:
        i, created = Industry.objects.get_or_create(id=industry[1])
        company.industry = i
        i.name = industry[0]
        if created:
            i.save()

    return company


def delete_db():
    print('truncate db')
    Company.objects.all().delete()
    Industry.objects.all().delete()
    print('finished truncate db')


def populate():
    industry_map = INDUSTRY

    cumsum = pd.Series(list(map(lambda x: x[2],industry_map))).cumsum()
    df = pd.read_csv(DATA_DIR + "companies.csv")
    print('company data loaded')

    bulk_list = []
    for (i, id, name) in tqdm(df.values.tolist()):
        try:
            idx = (cumsum > i).values.tolist().index(True)
            industry = industry_map[idx]
        except ValueError:
            industry = None
        finally:
            company = create_company(id, name, industry)
            bulk_list.append(company)

            if i % BATCH_SIZE == 0:
                Company.objects.bulk_create(bulk_list)
                bulk_list = []
            

def run():
    print("Starting Companies Population script...")
    delete_db()
    populate()