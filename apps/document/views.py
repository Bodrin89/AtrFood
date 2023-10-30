from django.http import HttpResponse
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from apps.document.models import DocumentModel


class DocumentDownloadView(APIView):
    """Скачивание документа по id"""

    def get(self, request, pk):
        document = get_object_or_404(DocumentModel, pk=pk)
        response = HttpResponse(document.file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{document.file}"'
        return response
