from userauth.models import Manager
from rest_framework import serializers


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'
