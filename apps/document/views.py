import os

from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView

from apps.document.models import DocumentModel


class DocumentDownloadView(APIView):
    """Скачивание документа по id"""

    def get(self, request, document_id):
        document = get_object_or_404(DocumentModel, pk=document_id)
        try:
            response = HttpResponse(document.file, content_type='application/octet-stream')
            filename = os.path.basename(document.file.name)
            encoded_filename = escape_uri_path(filename)
            response['Content-Disposition'] = f'attachment; filename="{encoded_filename}"'
            return response
        except FileNotFoundError:
            return Response(_('Файл не найден'))
