from rest_framework.views import APIView

from apps.document.services import ServiceDocument


class DocumentDownloadView(APIView):
    """Скачивание документа по id"""

    def get(self, request, document_id, type_file):
        return ServiceDocument.download_file(request, document_id, type_file)
