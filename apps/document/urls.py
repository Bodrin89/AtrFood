

from django.urls import path

from apps.document.views import DocumentDownloadView

urlpatterns = [
    path('<int:document_id>/download/', DocumentDownloadView.as_view(), name='document-download'),
]