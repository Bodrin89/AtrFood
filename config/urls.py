from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [

              ] + i18n_patterns(
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include(('apps.user.urls', 'apps.user'))),
    path('', include(('apps.individual_user.urls', 'apps.individual_user'))),
    path('', include(('apps.company_user.urls', 'apps.company_user'))),
    prefix_default_language=False,
)
