

from django.urls import path

from apps.document.views import DocumentDownloadView

urlpatterns = [
    path('<int:document_id>/<str:type_file>/download/', DocumentDownloadView.as_view(),
         name='document-download'),
]