import os

from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from apps.document.models import DocumentModel


class ServiceDocument:
    @staticmethod
    def download_file(request, document_id, type_file):
        """Скачивание файлов юридического лица"""
        document = get_object_or_404(DocumentModel, pk=document_id)

        if request.user.is_authenticated and request.user.pk == document.company_user.pk:
            if type_file == 'avr':
                file_field = document.file_avr.file_avr
            elif type_file == 'payment_invoice':
                file_field = document.file_payment_invoice
            else:
                return Response(_("Не верный тип файла"))

            try:
                response = HttpResponse(file_field, content_type='application/octet-stream')
                filename = os.path.basename(file_field.name)
                encoded_filename = escape_uri_path(filename)
                response['Content-Disposition'] = f'attachment; filename="{encoded_filename}"'
                return response
            except FileNotFoundError:
                return Response(_('Файл не найден'))
        else:
            return Response(_("У вас нет прав для скачивания этого файла"))
