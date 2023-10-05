from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.user.urls', 'apps.user'))),
    path('', include(('apps.individual_user.urls', 'apps.individual_user'))),
    path('', include(('apps.company_user.urls', 'apps.company_user'))),
]
