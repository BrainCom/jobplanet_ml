from tqdm import tqdm
from ...collector.models import CompanyPageView
from ...analytics.models import CompanyRating
from ...utils.helpers.list_helper import divide_chunks
import pandas as pd

BATCH_SIZE = 900
WEIGHT ={
	'landing': 1,
	'review': 1,
	'salary': 1,
	'interview': 2,
	'job_posting': 3,
	'job_posting_detail': 5,
	'benefit': 1,
	'analytics': 1,
	'etc': 1
}

def create_rating():
	s = sum(WEIGHT.values())
	weight = {k: v/s for k,v in WEIGHT.items()}

	arr = list(CompanyPageView.objects.values('customer_id', 'company_id', 'landing', 'review', 'salary', 'interview', 'job_posting', 'job_posting_detail', 'benefit', 'analytics', 'etc'))
	df = pd.DataFrame(arr)

	score = df.landing * weight['landing'] \
			+ df.review * weight['review'] \
			+ df.salary * weight['salary'] \
			+ df.interview * weight['interview'] \
			+ df.job_posting * weight['job_posting'] \
			+ df.job_posting_detail * weight['job_posting_detail'] \
			+ df.benefit * weight['benefit'] \
			+ df.analytics * weight['analytics'] \
			+ df.etc * weight['etc']


	df['score'] = score
	df = df.reindex(columns=['company_id', 'customer_id', 'score'])
	max_score = df.max()['score']
	df['score'] = df.score / max_score * 10

	df = df.drop_duplicates(['company_id','customer_id'])

	bulk_list = []
	for index, row in tqdm(df.iterrows()):
		rating = CompanyRating(customer_id=row['customer_id'],
							   company_id=row['company_id'],
							   rating=row['score'])
		bulk_list.append(rating)

	chunked = list(divide_chunks(bulk_list, BATCH_SIZE))
	for ch in tqdm(chunked):
	    CompanyRating.objects.bulk_create(ch)

def delete_db():
    print('truncate company rating db')
    CompanyRating.objects.all().delete()
    print('finished truncate company rating db')

def sync_rating():
    print("Starting Jobplanet Sync rating script...")
    delete_db()
    create_rating()

def run():
    sync_rating()