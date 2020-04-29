from tqdm import tqdm
from ...companies.models import Company, Industry
from ...jobplanet.models import Industry as JPIndustry
from ...jobplanet.models import Company as JPCompany
from ...utils.helpers.list_helper import divide_chunks

BATCH_SIZE = 900
# BATCH_SIZE = 3


def create_industry():
    print('create industry db')
    jp_industry = list(JPIndustry.objects.filter(active=1).order_by('parent_id'))
    arr =list(map(lambda a: Industry(id = a.id, name = a.name, parent_id = a.parent_id), jp_industry))
    
    Industry.objects.bulk_create(arr)
    print('finished industry db')

def create_company():
    print('create company db')
    bulk_list = []

    industries = list(Industry.objects.values_list('id', flat=True))
    companies = JPCompany.objects.exclude(name=None).exclude(industry_id=None).exclude(industry2_id=None)
    # companies = JPCompany.objects.exclude(name=None)

    for c in tqdm(companies):
        if c.industry2_id in industries:
            industry_id  = c.industry_id
            industry2_id = c.industry2_id
        else:
            industry_id = None
            industry2_id = None

        company = Company(id=c.id,
                          name=c.name,
                          industry_id=industry_id,
                          industry2_id=industry2_id)
        bulk_list.append(company)

    chunked = list(divide_chunks(bulk_list, BATCH_SIZE))
    for ch in tqdm(chunked):
        Company.objects.bulk_create(ch)

    print('finished customer db')

def delete_db():
    print('truncate company db')
    Company.objects.all().delete()
    Industry.objects.all().delete()
    print('finished truncate company db')


def sync_company():
    print("Starting Jobplanet Sync script...")
    delete_db()
    create_industry()
    create_company()


def run():
    sync_company()
    
