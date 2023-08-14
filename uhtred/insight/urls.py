from . import views
from uhtred.core.urls import Router


app_name = 'insight'

router = Router(False)
router.register('insights', views.InsightViewSet, 'insight')

urlpatterns: list = []

urlpatterns = urlpatterns + router.urls
