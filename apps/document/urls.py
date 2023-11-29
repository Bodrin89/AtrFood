

from django.urls import path

from apps.document.views import DocumentDownloadView, ListDocumentView

urlpatterns = [
    path('<int:document_id>/<str:type_file>/download/', DocumentDownloadView.as_view(),
         name='document-download'),
    path('list', ListDocumentView.as_view(), name='list-documents'),
]