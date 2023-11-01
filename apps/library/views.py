from rest_framework.generics import ListAPIView
from apps.library.models import PrivacyPolicy, ReturnPolicy, AboutCompany
from apps.library.serializers import ReturnPolicySerializer, PrivacyPolicySerializer, AboutCompanySerializer


class PrivacyPolicyView(ListAPIView):
    serializer_class = PrivacyPolicySerializer
    queryset = PrivacyPolicy.objects.all()


class ReturnPolicyView(ListAPIView):
    serializer_class = ReturnPolicySerializer
    queryset = ReturnPolicy.objects.all()


class AboutCompanyView(ListAPIView):
    serializer_class = AboutCompanySerializer
    queryset = AboutCompany.objects.all()