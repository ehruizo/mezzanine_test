from rest_framework import viewsets
from .models import DbtestUsers, DbtestInvoices, DbtestPurchases
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DbtestUsers.objects.all()
    serializer_class = UserSerializer
