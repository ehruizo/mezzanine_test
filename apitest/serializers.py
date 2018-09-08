from rest_framework import serializers
from .models import DbtestUsers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DbtestUsers
        fields = ('document', 'first_name', 'last_name', 'birth_date')
