from tqdm import tqdm
from ...customers.models import Customer, Occupation
from ...jobplanet.models import Occupation as JPOccupation
from ...jobplanet.models import User, UserInfo
from ...utils.helpers.list_helper import divide_chunks

BATCH_SIZE = 900
# BATCH_SIZE = 3


def create_occupation():
    print('create occupation db')
    jp_occu = list(JPOccupation.objects.filter(active=1).order_by('parent_id'))
    arr =list(map(lambda a: Occupation(id = a.id, name = a.name, parent_id = a.parent_id), jp_occu))
    
    Occupation.objects.bulk_create(arr)
    print('finished occupation db')

def create_customer():
    print('create customer db')
    bulk_list = []

    occupations = list(Occupation.objects.values_list('id', flat=True))
    users = User.objects.exclude(quit_at=1).prefetch_related('userinfo_set')

    for u in tqdm(users):
        occupation_id = None
        occupation2_id = None

        u_info_set = u.userinfo_set.filter(question_id=147).order_by('-updated_at')
        if u_info_set:
            u_info = u_info_set[0]
            if u_info.occupation_id in occupations:
                occupation_id  = u_info.occupation.parent_id
                occupation2_id = u_info.occupation_id

        customer = Customer(id=u.id,
                            name=u.name,
                            occupation_id=occupation_id,
                            occupation2_id=occupation2_id)
        bulk_list.append(customer)

    chunked = list(divide_chunks(bulk_list, BATCH_SIZE))
    for ch in tqdm(chunked):
        Customer.objects.bulk_create(ch)

    print('finished customer db')

def delete_db():
    print('truncate customer db')
    Customer.objects.all().delete()
    Occupation.objects.all().delete()
    print('finished truncate customer db')


def sync_customer():
    print("Starting Jobplanet Sync Customer script...")
    delete_db()
    create_occupation()
    create_customer()


def run():
    sync_customer()