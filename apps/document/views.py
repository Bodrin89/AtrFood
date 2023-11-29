from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.document.models import DocumentModel
from apps.document.serializers import DocumentSerializer
from apps.document.services import ServiceDocument



class DocumentDownloadView(APIView):
    """Скачивание документа по id"""

    def get(self, request, document_id, type_file):
        return ServiceDocument.download_file(request, document_id, type_file)


class ListDocumentView(ListAPIView):
    """Получение всех документов"""
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return DocumentModel.objects.filter(company_user=self.request.user.id)
