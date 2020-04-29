from config import celery_app
from celery import chain
# from .scripts.calc_user_cluster import UserClusterCalculator
# from .scripts.calc_item_similar import ItemSimilarityMatrixBuilder, load_all_ratings
from .scripts.jobplanet_sync import sync_all
from .scripts.jobplanet_sync_posting import sync_posting
from .scripts.jobplanet_sync_customer import sync_customer
from .scripts.jobplanet_sync_company import sync_company
from .scripts.jobplanet_sync_collector import sync_collector
from .scripts.jobplanet_sync_rating import sync_rating
from .scripts.surprise_similar_train import train_model
from .scripts.surprise_similar_calc import precalc_model


# @celery_app.task()
# def calculate_cluster():
# 	cluster = UserClusterCalculator()
# 	cluster.calculate(23)


# @celery_app.task()
# def calculate_item_similarity():
# 	print("Calculation of item similarity")

# 	all_ratings = load_all_ratings()
# 	ItemSimilarityMatrixBuilder(min_overlap=5, min_sim=0.0).build(all_ratings)

# for sample test
@celery_app.task()
def add(x, y):
    return x + y

@celery_app.task()
def train_similar_company(industry_id, sample_size=None):
	return train_model(industry_id=industry_id, sample_size=sample_size)


@celery_app.task()
def calc_similar_company(industry_id):
	return precalc_model(industry_id=industry_id)


@celery_app.task()
def jobplanet_sync_collector():
	return sync_collector()


@celery_app.task()
def jobplanet_sync_rating(response=None):
	return sync_rating()


@celery_app.task()
def jobplanet_sync_all():
	return sync_all()


@celery_app.task()
def jobplanet_sync_posting():
	return sync_posting()


@celery_app.task()
def jobplanet_sync_customer():
	return sync_customer()


@celery_app.task()
def jobplanet_sync_company():
	return sync_company()


