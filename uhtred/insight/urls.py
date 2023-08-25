from . import views
from django.urls import path
from uhtred.core.urls import Router


app_name = 'insight'

router = Router(False)
router.register('insights', views.InsightViewSet, 'insight')

urlpatterns: list = [
    path('insights/draft/<int:insight_id>', views.draft_preview)
]

urlpatterns = urlpatterns + router.urls
