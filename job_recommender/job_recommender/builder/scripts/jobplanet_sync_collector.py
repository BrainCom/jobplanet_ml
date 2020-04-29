from tqdm import tqdm
from ...collector.models import CompanyPageView
from ...customers.models import Customer
from ...companies.models import Company
from ...utils.helpers.list_helper import divide_chunks
from ...utils.connections import DBConnection
import random
import datetime
from django.utils import timezone
import math

MAX_PRESTO_CHUNK_SIZE = 1000
# MAX_PRESTO_CHUNK_SIZE = 2
BATCH_SIZE = 900

def create_fake_collector():
	bulk_list = []
	AVG_PV = 100

	all_users = Customer.objects.all()
	all_companies = Company.objects.all()
	num_users = len(all_users)
	num_companies = len(all_companies)

	company_samples = Company.objects.all()[:1000].values_list('id', flat=True)

	for i in tqdm(range(num_users)):
		for j in range(AVG_PV):
			nums = random.sample(range(100), 9)
			pv = CompanyPageView(customer_id=all_users[i].id,
								company_id=company_samples[j],
								landing=nums[0],
								review=nums[1],
								salary=nums[2],
								interview=nums[3],
								job_posting=nums[4],
								job_posting_detail=nums[5],
								benefit=nums[6],
								analytics=nums[7],
								etc=nums[8],
								total=sum(nums))
			bulk_list.append(pv)

	chunked = list(divide_chunks(bulk_list, BATCH_SIZE))
	for ch in tqdm(chunked):
	    CompanyPageView.objects.bulk_create(ch)


def get_query(user_ids):
	if len(user_ids) > MAX_PRESTO_CHUNK_SIZE:
		raise Exception('user_ids is too big!')

	now = timezone.localtime()
	month_ago = datetime.date.today() - datetime.timedelta(1*365/12)
	return ("""
		SELECT 
		    a.user_id as user_id,
		    b.id as company_id,
		    count_if(controller IN ('CompaniesController', 'API::V1::CompaniesController') AND action IN ('show', 'summary')) AS landing,
		    count_if(controller IN ('CompaniesController', 'API::V1::CompaniesController') AND action IN ('reviews')) AS review,
		    count_if(controller IN ('CompaniesController', 'API::V1::CompaniesController') AND action IN ('salaries')) AS salary,
		    count_if(controller IN ('CompaniesController', 'API::V1::CompaniesController') AND action IN ('interviews')) AS interview,
		    count_if(controller IN ('CompaniesController', 'API::V2::CompaniesController') AND action IN ('job_postings')) AS job_posting,
		    count_if(controller IN ('CompaniesController', 'API::V2::CompaniesController') AND action IN ('job_posting_detail')) AS job_posting_detail,
		    count_if(controller IN ('CompaniesController', 'API::V1::CompaniesController') AND action IN ('benefits', 'benefit_details')) AS benefit,
		    count_if(controller IN ('CompaniesController', 'API::V1::CompaniesController') AND action IN ('analytics')) AS analytics,
		    count_if(action NOT IN ('show', 'reviews', 'salaries', 'interviews', 'job_postings', 'job_posting_detail', 'benefits', 'benefit_details', 'analytics', 'summary')) AS etc
		from hive.ko.jplog_map AS a
		JOIN ko_jpdb.jobplanet.companies AS b
			ON cast(b.id as varchar) = a.params['id']
		WHERE cast(a.user_id as integer) IN ({user_ids})
			and date_parse(a.dt,'%Y%m%d') BETWEEN from_iso8601_timestamp(concat('{begin_dt:%Y-%m-%d}', 'T00:00:00+09:00')) 
										  AND from_iso8601_timestamp(concat('{end_dt:%Y-%m-%d}', 'T00:00:00+09:00'))
			and from_iso8601_timestamp(a.access_time) BETWEEN from_iso8601_timestamp(concat('{begin_dt:%Y-%m-%d}', 'T00:00:00+09:00')) 
													  AND from_iso8601_timestamp(concat('{end_dt:%Y-%m-%d}', 'T00:00:00+09:00'))
			and a.controller IN ('CompaniesController', 'API::V1::CompaniesController', 'API::V2::CompaniesController')
		GROUP BY 1,2
		ORDER BY 1,2
		LIMIT 300000
	""".format(
			user_ids=",".join(map(str,user_ids)),
			begin_dt=month_ago,
			end_dt=now
		))

def save_pageview(customer_ids, rows):
	bulk_list = []
	log_company_ids = set(map(lambda x: int(x[1]), rows))
	company_ids = list(Company.objects.filter(id__in=log_company_ids).values_list('id', flat=True))

	for r in rows:
		if int(r[1]) not in company_ids:
			continue

		pv = CompanyPageView(customer_id=r[0],
							company_id=r[1],
							landing=r[2],
							review=r[3],
							salary=r[4],
							interview=r[5],
							job_posting=r[6],
							job_posting_detail=r[7],
							benefit=r[8],
							analytics=r[9],
							etc=r[10],
							total=sum(r[2:]))
		bulk_list.append(pv)

	CompanyPageView.objects.filter(customer_id__in=customer_ids).delete()
	CompanyPageView.objects.bulk_create(bulk_list)


def create_collector():
	customer_ids = list(Customer.objects.all().values_list('id', flat=True))
	group_no = math.ceil(len(customer_ids)/MAX_PRESTO_CHUNK_SIZE)

	conn = DBConnection(db='presto')
	cur = conn.cursor
	for no in range(group_no):
		lo = no*MAX_PRESTO_CHUNK_SIZE
		hi = lo + MAX_PRESTO_CHUNK_SIZE
		chunked = customer_ids[lo:hi]

		sql = get_query(chunked)
		print(sql)
		
		cur.execute(sql)
		rows = cur.fetchall()

		save_pageview(chunked, rows)


def delete_db():
    print('truncate collector db')
    CompanyPageView.objects.all().delete()
    print('finished truncate collector db')

def sync_collector():
    print("Starting Jobplanet Sync Collector script...")
    create_collector()

def run():
    sync_collector()