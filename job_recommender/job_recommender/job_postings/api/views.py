from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import PostingSerializer
from ..models import Posting
from ...customers.models import Customer
from ...scores.models import CompanySimilarity



class PostingViewSet(GenericViewSet):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer

    @action(detail=False, url_path='(?P<customer_id>[0-9]+)/company/(?P<company_id>[0-9]+)/similar/(?P<k>[0-9]+)')
    def similar_company(self, request, customer_id=None, company_id=None, k=None, occupation_id=None):
        customer = Customer.objects.filter(id=customer_id).first()
        if customer:
        	occupation_id = customer.occupation_id

        if occupation_id:
        	qs = self.queryset.filter(
	    	    postingoccupation__occupation_id=occupation_id,
	    	    company__sim_target__source_id=company_id,
	    	    company__sim_target__formula='pearson',
        	).order_by('-company__sim_target__similarity')[:int(k)]
        else:
        	qs = self.queryset.filter(
	    	    company__sim_target__source_id=company_id,
	    	    company__sim_target__formula='pearson'
        	).order_by('-company__sim_target__similarity')[:int(k)]


        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)