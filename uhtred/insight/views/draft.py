from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from uhtred.insight.models import Insight
from uhtred.insight.serializers import InsightDetail


@api_view(['GET'])
def draft_preview(request: Request, insight_id: int) -> Response:
    insight: Insight = get_object_or_404(
        Insight,
        published_at__isnull=True,
        id=insight_id)
    serializer = InsightDetail(insight)
    return Response(serializer.data)
