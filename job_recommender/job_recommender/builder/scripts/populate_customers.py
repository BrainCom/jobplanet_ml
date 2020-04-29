import os
from tqdm import tqdm
import pandas as pd
from ...customers.models import Customer, Occupation

BATCH_SIZE = 900
DATA_DIR="job_recommender/builder/scripts/data/"
OCCUPATION_LABEL = ["경영/기획/컨설팅", "마케팅/시장조사", "영업/제휴", "서비스/고객지원", "미디어/홍보", "교육", "법률/법무", "인사/총무", "금융/재무", "의약", "생산/제조", "생산관리/품질관리", "엔지니어링", "연구개발", "유통/무역", "IT/인터넷", "디자인", "전문직", "특수계층/공공"]
OCCUPATION = [
    [10100, 63302],
    [10200, 48652],
    [10300, 60519],
    [10400, 50553],
    [10500, 31316],
    [10600, 26140],
    [10700, 6998],
    [10800, 40964],
    [10900, 49021],
    [11000, 13285],
    [11100, 59190],
    [11200, 46002],
    [11300, 44277],
    [11400, 54912],
    [11500, 43799],
    [11600, 119474],
    [11700, 66114],
    [11800, 15253],
    [11900, 10822]
]


def create_customer(id, occupation = None):
    customer = Customer(id=id)

    if occupation:
        occu, created = Occupation.objects.get_or_create(id=occupation[1])
        customer.occupation = occu
        occu.name = occupation[0]
        if created:
            occu.save()

    return customer


def delete_db():
    print('truncate db')
    Customer.objects.all().delete()
    Occupation.objects.all().delete()
    print('finished truncate db')


def populate():
    occupations = list(map(lambda i: [OCCUPATION_LABEL[i]] + OCCUPATION[i], range(len(OCCUPATION))))
    cumsum = pd.Series(list(map(lambda x: x[2], occupations))).cumsum()

    df = pd.read_csv(DATA_DIR + "customers.csv")
    print('customer data loaded')

    bulk_list = []
    for (i, id) in tqdm(df.values.tolist()):
        try:
            idx = (cumsum > i).values.tolist().index(True)
            occu = occupations[idx]
        except ValueError:
            occu = None
        finally:
            customer = create_customer(id, occu)
            bulk_list.append(customer)

            if i % BATCH_SIZE == 0:
                Customer.objects.bulk_create(bulk_list)
                bulk_list = []


def run():
    print("Starting Customers Population script...")
    delete_db()
    populate()
