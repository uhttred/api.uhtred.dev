from . import views
from uhtred.core.urls import Router


app_name = 'newsletter'

router = Router(False)
router.register('emails', views.EmailListViewSet, 'email')

urlpatterns: list = []

urlpatterns = urlpatterns + router.urls
