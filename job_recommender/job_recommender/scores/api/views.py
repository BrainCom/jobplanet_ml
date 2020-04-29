from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CompanySimilaritySerializer
from ..models import CompanySimilarity

class CompanySimilarityViewSet(GenericViewSet):
    queryset = CompanySimilarity.objects.all()
    serializer_class = CompanySimilaritySerializer

    @action(detail=False, url_path='(?P<company_id>[0-9]+)/similar/(?P<k>[0-9]+)')
    def top_k(self, request, company_id=None, k=None):
        qs = self.queryset.filter(source_id=company_id, formula='pearson').order_by('-similarity')[:int(k)]
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)