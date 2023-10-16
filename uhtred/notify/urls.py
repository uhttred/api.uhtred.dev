from . import views
# from django.urls import path
from uhtred.core.urls import Router


app_name = 'notify'

router = Router(False)
router.register('notify/emails', views.EmailViewSet, 'emails')

urlpatterns: list = []

urlpatterns = urlpatterns + router.urls
