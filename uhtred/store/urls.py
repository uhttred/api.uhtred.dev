from . import views
from uhtred.core.urls import Router


app_name = 'store'

router = Router(False)
router.register('products', views.ProductViewSet, 'product')

urlpatterns: list = []

urlpatterns = urlpatterns + router.urls
