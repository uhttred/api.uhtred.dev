from . import views
from uhtred.core.urls import Router


app_name = 'base'

router = Router(False)
router.register('tags', views.TagViewSet, 'tag')

urlpatterns: list = []

urlpatterns = urlpatterns + router.urls
