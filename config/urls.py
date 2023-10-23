from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [

              ] + i18n_patterns(
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/user/', include(('apps.user.urls', 'apps.user'))),
    path('api/', include(('apps.individual_user.urls', 'apps.individual_user'))),
    path('api/', include(('apps.company_user.urls', 'apps.company_user'))),
    path('api/', include(('apps.product.urls', 'apps.product'))),
    path('api/review/', include(('apps.review.urls', 'apps.review'))),
    path('api/', include(('apps.cart.urls', 'apps.cart'))),
    path('api/order/', include(('apps.order.urls', 'apps.order'))),
    prefix_default_language=True,
)
