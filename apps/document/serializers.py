
from rest_framework import serializers

from apps.document.models import DocumentModel, AvrFileModel


class FileAVRSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvrFileModel
        fields = ('file_avr', 'name')


class DocumentSerializer(serializers.ModelSerializer):

    file_avr = FileAVRSerializer()

    class Meta:
        model = DocumentModel
        fields = ('file_avr', 'file_payment_invoice', 'company_user', 'name')



