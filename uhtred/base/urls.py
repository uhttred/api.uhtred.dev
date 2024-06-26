from . import views
from uhtred.core.urls import Router


app_name = 'base'

router = Router(False)
router.register('tags', views.TagViewSet, 'tag')
router.register('person', views.PersonViewSet, 'person')
router.register('quotes', views.QuoteViewSet, 'quote')

urlpatterns: list = []

urlpatterns = urlpatterns + router.urls
