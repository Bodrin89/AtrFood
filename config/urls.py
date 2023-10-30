from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [

              ] + i18n_patterns(
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/user/', include(('apps.user.urls', 'apps.user'))),
    path('api/', include(('apps.individual_user.urls', 'apps.individual_user'))),
    path('api/', include(('apps.company_user.urls', 'apps.company_user'))),
    path('api/products/', include(('apps.product.urls', 'apps.product'))),
    path('api/review/', include(('apps.review.urls', 'apps.review'))),
    path('api/cart/', include(('apps.cart.urls', 'apps.cart'))),
    path('api/order/', include(('apps.order.urls', 'apps.order'))),
    path('api/discounts/', include(('apps.promotion.urls', 'apps.promotion'))),
    path('api/documents/', include(('apps.document.urls', 'apps.document'))),

    prefix_default_language=True,
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
