from rest_framework.views import APIView

from apps.product.services import ServiceProduct


class DocumentDownloadView(APIView):
    """Скачивание документа по id"""

    def get(self, request, document_id, type_file):
        return ServiceProduct.download_file(request, document_id, type_file)
