from tqdm import tqdm
from ...jobplanet.models import JobPosting
from ...job_postings.models import Posting, PostingOccupation
from ...companies.models import Company
import datetime

def create_posting():
	month_ago = datetime.date.today() - datetime.timedelta(1*365/12)
	job_postings = JobPosting.objects.filter(status=JobPosting.STATUS.PUBLISHED, end_at__gte=month_ago) \
									 .prefetch_related('postingoccupation_set') \
									 .select_related('company')

	for j in tqdm(job_postings):
		if Company.objects.filter(id=j.company_id).exists():
			occupation_ids = list(j.postingoccupation_set.values_list('occupation_id', flat=True))
			posting = Posting.objects.create(id=j.id,
											 name=j.name,
											 company_id=j.company_id,
											 start_at=j.start_at,
											 end_at=j.end_at)

			for occu in occupation_ids:
				PostingOccupation.objects.create(posting=posting, occupation_id=occu)


def delete_db():
    print('truncate posting db')
    Posting.objects.all().delete()
    PostingOccupation.objects.all().delete()
    print('finished truncate posting db')

def sync_posting():
    print("Starting Jobplanet Sync Posting script...")
    delete_db()
    create_posting()

def run():
    sync_posting()