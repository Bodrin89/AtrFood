
from rest_framework import serializers

from apps.document.models import DocumentModel


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentModel
        fields = '__all__'



