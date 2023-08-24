from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include


admin.site.site_url = 'https://uhtred.dev'  # Removes the 'View Site' link
admin.site.site_header = _('Uhtred Administration')
admin.site.site_title = _('Uhtred Administration')
admin.site.index_title = 'Uhtred'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('martor/', include('martor.urls')),
    path('newsletter/', include('uhtred.newsletter.urls')),
    path('', include('uhtred.insight.urls')),
    path('', include('uhtred.case.urls')),
    path('', include('uhtred.store.urls')),
    path('', include('uhtred.base.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
    