from django.http import JsonResponse
from celery import chain
from ..companies.models import Industry
from .tasks import (
    jobplanet_sync_all,
    jobplanet_sync_posting,
    jobplanet_sync_customer,
    jobplanet_sync_company,
    jobplanet_sync_collector,
    jobplanet_sync_rating,
    train_similar_company,
    calc_similar_company,
    add
)

def test(request):
    add.apply_async(args=[1,2])
    return JsonResponse({'success' : 1})


# TRAIN QUEUE    
def train_calc_similar_company(request):
    industry_ids = Industry.objects.filter(parent_id=None).values_list('id', flat=True)
    for id in industry_ids:
        chained = chain(
            train_similar_company.s(id, sample_size=5000),
            calc_similar_company.s()
        )
        chained.apply_async()

    return JsonResponse({'success' : 1})


# COLLECT QUEUE
def collect_rate_companyview(request):
    chained = chain(
        jobplanet_sync_collector.s(),
        jobplanet_sync_rating.s()
    )
    chained.apply_async()

    return JsonResponse({'success' : 1})


def sync_collector(request):
    jobplanet_sync_collector.apply_async()
    return JsonResponse({'success' : 1})


def sync_rating(request):
    jobplanet_sync_rating.apply_async()
    return JsonResponse({'success' : 1})


# SYNC QUEUE     
def sync_all(request):
    jobplanet_sync_all.apply_async()
    return JsonResponse({'success' : 1})


def sync_customer(request):
    jobplanet_sync_customer.apply_async()
    return JsonResponse({'success' : 1})


def sync_company(request):
    jobplanet_sync_company.apply_async()
    return JsonResponse({'success' : 1})


def sync_posting(request):
    jobplanet_sync_posting.apply_async()
    return JsonResponse({'success' : 1})



