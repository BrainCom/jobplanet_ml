from .jobplanet_sync_customer import sync_customer
from .jobplanet_sync_company import sync_company
from .jobplanet_sync_posting import sync_posting
from .jobplanet_sync_cronjobs import sync_periodic_task

def sync_all():
    print("Starting Jobplanet Sync script...")
    sync_customer()
    sync_company()
    sync_posting()
    sync_periodic_task()


def run():
    sync_all()
