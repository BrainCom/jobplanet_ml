from django_celery_beat.models import CrontabSchedule, PeriodicTask


def get_schedule(name):
	if name is 'refresh_job_postings':
		schedule, _ = CrontabSchedule.objects.get_or_create(
			minute='0',
			hour='4',
			day_of_week='*',
			day_of_month='*',
			month_of_year='*',
			timezone='Asia/Seoul'
		)
	else:
		schedule = None


	return schedule



def register_periodic_task():
	schedule = get_schedule('refresh_job_postings')

	if schedule:
		PeriodicTask.objects.create(
			crontab=schedule,
			name='Refresh Job Postings',
			task='job_recommender.builder.tasks.jobplanet_sync_posting',
			queue='cron'
		)


def delete_db():
    print('truncate periodic_task db')
    PeriodicTask.objects.exclude(name='celery.backend_cleanup').delete()
    print('finished truncate periodic_task db')

def sync_periodic_task():
    print("Starting Jobplanet Sync Collector script...")
    delete_db()
    register_periodic_task()

def run():
    sync_periodic_task()