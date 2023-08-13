from . import views
from uhtred.core.urls import Router


app_name = 'case'

router = Router(False)
router.register('cases', views.CaseViewSet, 'case')

urlpatterns: list = []

urlpatterns = urlpatterns + router.urls
